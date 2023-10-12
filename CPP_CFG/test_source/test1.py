from antlr4 import *
from antlr4 import TokenStreamRewriter
from gen.CPP14_v2Listener import CPP14_v2Listener
from gen.CPP14_v2Parser import CPP14_v2Parser
from gen.CPP14_v2Lexer import CPP14_v2Lexer as lexer

import networkx as nx
import matplotlib.pyplot as plt
import json
SWITCH_FOR = {
    "for_while" : 0,
    "range_for" : 1,
    "switch" : 2
}
class CFGInstListener(CPP14_v2Listener):

    def addNode(self):
        try:
            if not self.is_catch:
                self.try_stack[-1].add((self.block_number , 'exception'))
        except:
            pass
        self.block_dict[self.domain_name]["Nodes"].append((self.block_number, self.block_start, self.block_stop))

    def insertAfter(self, ctx):
        new_code = '\n' + self.logLine() + ';\n'
        self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex, new_code)

    def logLine(self):
        return 'logFile << "' + str(self.domain_name) + ' ' + str(self.block_number) + '" << std::endl'

    def addJunctionEdges(self):
        for source_node,Type  in self.select_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node,Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')
    def addDecisionEdge(self):
        source_node,Type = self.select_decision_stack.pop()
        dest_node = self.block_number
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node,Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addJunc(self , Type = 'flow'):
        self.select_junction_stack[-1].append((self.block_number , Type))

    def addDecision(self , Type = 'flow'):
        self.select_decision_stack.append((self.block_number , Type))
    def __init__(self, common_token_stream: CommonTokenStream, number_of_tokens , directory_name):
        """
        :param common_token_stream:
        """
        self.cfg_path = 'CFGS/' + directory_name + '/'
        self.instrument_path = 'Instrument/' + directory_name + '/'
        self.block_dict = {}
        self.block_number = 0
        self.block_start = 0
        self.block_stop = 0
        self.domain_name = 0
        self.function_dict = {}
        self.select_junction_stack = []
        self.select_decision_stack = []
        self.iterate_junction_stack = []
        self.iterate_stack = []
        self.switch_junction_stack = []
        self.switch_stack = []
        self.switch_for_stack = []
        self.has_jump_stack = []
        self.has_default_stack = []
        self.has_case_stack = []
        self.try_stack = []
        self.try_junction_stack = []
        self.is_catch = False
        self.afterInsert = [''] * number_of_tokens
        self.initial_nodes = set()
        self.final_nodes = set()
        self.label_dict = {}
        self.goto_dict = {}

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter.TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        # create graph
        self.CFG_graph = nx.Graph()

    def enterFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):
        self.initial_nodes = set()
        self.final_nodes = set()
        temp = ctx.declarator().getText().replace('~', "destructor")
        function_name = ''.join(c for c in temp if c.isalnum())
        self.domain_name += 1
        self.function_dict[self.domain_name] = (function_name , ctx.start.line)
        self.block_dict[self.domain_name] = {
            "Nodes": [],
            "Edges": []
        }
        self.CFG_file = open(self.cfg_path + str(self.domain_name) + '.txt', 'w')


    def enterFunctionbody1(self, ctx:CPP14_v2Parser.Functionbody1Context): #normal function
        self.block_number = 1
        self.block_start = ctx.start.line
        self.has_jump_stack.append(False)
        self.insertAfter(ctx)
        self.initial_nodes.add(self.block_number)

    def enterSelectionstatement1(self, ctx:CPP14_v2Parser.Selectionstatement1Context): #if
        self.block_stop = ctx.start.line
        self.addNode()
        print(self.block_stop)
        self.select_junction_stack.append(list())
        #self.addInitEdge()
        print(self.select_junction_stack)
        print(self.block_number)
        self.addDecision('TrueEr')
        print("dec : ")
        print(self.addDecision())
        print(self.block_number)
        self.addJunc('FalseEr')
        print("junc : ")
        print(self.addJunc())
        print(self.block_number)
        print("pt1 End \n _____________________________")
    def enterStatement(self, ctx:CPP14_v2Parser.StatementContext):
        if isinstance(ctx.parentCtx,(CPP14_v2Parser.Selectionstatement1Context , CPP14_v2Parser.Selectionstatement2Context)):
            self.block_number += 1
            print("test mid : " )
            print(self.block_number)
            self.addDecisionEdge()
            print(self.addDecisionEdge())
            self.block_start  = ctx.start.line
            print(self.block_start)
            self.has_jump_stack.append(False)
            print(self.has_jump_stack)
            # if there is a compound statement after the branchning condition:
            body = ctx.compoundstatement()
            if body != None:
                self.insertAfter(body)
            # if there is only one statement after the branchning condition then create a block.
            else:
                new_code = '{'
                new_code += '\n' + self.logLine() + ';\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
            print("End pt2 \n __________________________________")

    def exitStatement(self, ctx: CPP14_v2Parser.StatementContext):

        if isinstance(ctx.parentCtx,
                        (CPP14_v2Parser.Selectionstatement1Context, CPP14_v2Parser.Selectionstatement2Context)): # if
            self.block_stop = ctx.stop.line
            self.addNode()
            if not self.has_jump_stack.pop():
                self.addJunc()
            if ctx.compoundstatement() == None:
                new_code = '\n}'
                self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitSelectionstatement1(self, ctx: CPP14_v2Parser.Selectionstatement1Context):  # if
            print(self.block_number)
            self.block_number += 1
            print(self.block_number)
            self.block_start = ctx.stop.line
            print(self.block_start)
            tx = self.addJunctionEdges()
            print(tx)
            ty = self.select_junction_stack.pop()
            print(ty)
            new_code = '\n' + self.logLine() + ';\n'
            self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):
                initial_nodes_str = ' '.join(str(node) for node in self.initial_nodes)
                self.CFG_file.write("initial nodes:" + initial_nodes_str + '\n')
                self.final_nodes.add(self.block_number)
                final_nodes_str = ' '.join(str(node) for node in self.final_nodes)
                self.CFG_file.write("final nodes:" + final_nodes_str + '\n')
                print(self.block_dict)
                self.CFG_file.close()
                func_graph = nx.Graph()
                func_graph.add_nodes_from([n for n, s, e in self.block_dict[self.domain_name]["Nodes"]])
                func_graph.add_edges_from([(s, d) for s, d, T in self.block_dict[self.domain_name]["Edges"]])
                edge_labels = {}
                for s, d, T in self.block_dict[self.domain_name]["Edges"]:
                    edge_labels[(s, d)] = T
                nx.draw(func_graph, pos=nx.spring_layout(func_graph), with_labels=True)
                plt.savefig(self.cfg_path + str(self.domain_name) + '.png')
                plt.close()

                graph_json = open(self.cfg_path + str(self.domain_name) + '.json', 'w')
                json.dump(self.block_dict[self.domain_name], graph_json)

    def exitTranslationunit(self, ctx: CPP14_v2Parser.TranslationunitContext):
                """
                Creating and open a text file for logging the instrumentation result
                :param ctx:
                :return:
                """
                for i in range(len(self.afterInsert)):
                    if self.afterInsert[i] != '':
                        self.token_stream_rewriter.insertAfter(i, self.afterInsert[i])
                self.instrumented_source.write(self.token_stream_rewriter.getDefaultText())
                self.instrumented_source.close()

                functions_json = open(self.cfg_path + 'functions.json', 'w')
                json.dump(self.function_dict, functions_json)

    def enterDeclarator(self, ctx: CPP14_v2Parser.DeclaratorContext):
                pass
                # print(ctx.parentCtx.parentCtx.parentCtx.getText())
    def enterTranslationunit(self, ctx: CPP14_v2Parser.TranslationunitContext):
                """
                Creating and open a text file for logging the instrumentation result
                :param ctx:
                :return:
                """
                self.instrumented_source = open(self.instrument_path + 'instrumented_source.cpp', 'w')
                log_path = self.instrument_path + "log_file.txt"
                new_code = '\n//in the name of allah\n#include <fstream>\nstd::ofstream logFile("log_file.txt");\n\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
                self.domain_name = 0

    def exitFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):
        initial_nodes_str = ' '.join(str(node) for node in self.initial_nodes)
        self.CFG_file.write("initial nodes:" + initial_nodes_str + '\n')
        self.final_nodes.add(self.block_number)
        final_nodes_str = ' '.join(str(node) for node in self.final_nodes)
        self.CFG_file.write("final nodes:" + final_nodes_str + '\n')
        print(self.block_dict)
        self.CFG_file.close()
        func_graph = nx.Graph()
        func_graph.add_nodes_from([n for n,s,e in self.block_dict[self.domain_name]["Nodes"]])
        func_graph.add_edges_from([(s,d) for s,d,T in self.block_dict[self.domain_name]["Edges"]])
        edge_labels = {}
        for s,d,T in self.block_dict[self.domain_name]["Edges"]:
            edge_labels[(s,d)] = T
        nx.draw(func_graph , pos=nx.spring_layout(func_graph) , with_labels=True)
        plt.savefig(self.cfg_path + str(self.domain_name) + '.png')
        plt.close()

        graph_json = open(self.cfg_path + str(self.domain_name) + '.json' , 'w')
        json.dump(self.block_dict[self.domain_name] , graph_json)