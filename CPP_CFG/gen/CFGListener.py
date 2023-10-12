# in the name of allah

from antlr4 import *
from antlr4 import TokenStreamRewriter
from .CPP14_v2Listener import CPP14_v2Listener
from .CPP14_v2Parser import CPP14_v2Parser
from .CPP14_v2Lexer import CPP14_v2Lexer as lexer
import graphviz as gv
from itertools import islice
import networkx as nx
import html

import matplotlib.pyplot as plt
import json

SWITCH_FOR = {
    "for_while": 0,
    "range_for": 1,
    "switch": 2
}


class CFGInstListener(CPP14_v2Listener):

    def addNode(self):
        try:
            if not self.is_catch:
                self.try_stack[-1].add((self.block_number, 'exception'))
        except:
            pass

        temp = []
        temp = self.block_dict[self.domain_name]["Nodes"]
        if (len(temp) != 0):
            if (temp[-1][0] == self.block_number):
                return

        self.block_dict[self.domain_name]["Nodes"].append((self.block_number, self.block_start, self.block_stop))

        self.block_dict_tokens[self.domain_name]["Nodes"].append(
            (self.block_number, self.block_tstart, self.block_tstop))

    # def addNode(self):
    #    self.block_dict_tokens[self.domain_name]["Nodes"].append((self.block_number, self.block_tstart, self.block_tstop))
    def addJunctionEdges(self):
        for source_node, Type in self.select_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addJunctionEdges_for(self):
        for source_node, Type in self.select_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, 'Flow'))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addDecisionEdge(self):
        source_node, Type = self.select_decision_stack.pop()
        dest_node = self.block_number
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addJunc(self, Type='flow'):
        self.select_junction_stack[-1].append((self.block_number, Type))

    def addDecision(self, Type='flow'):
        self.select_decision_stack.append((self.block_number, Type))

    def addIterateJunctionEdges(self):
        for source_node, Type in self.iterate_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addIterateJunctionEdges_dwhile(self):
        for source_node, Type in self.iterate_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((dest_node, source_node + 1, 'flow'))
            self.CFG_file.write(str(dest_node) + ' ' + str(source_node + 1) + '\n')

    def addIterateEdge(self):
        source_node = self.block_number
        dest_node, Type = self.iterate_stack[-1]
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addIterateEdge_dwhile(self):
        source_node = self.block_number
        dest_node, Type = self.iterate_stack_d[-1]
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node + 1, Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node + 1) + '\n')

    def addInitEdge(self, Type='flow'):
        source_node = self.block_number
        dest_node = source_node + 1
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addDoWhileInitEdge(self):
        source_node = self.block_number
        dest_node = source_node + 1
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, 'flow'))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addIterateJunc(self, Type='flow'):
        self.iterate_junction_stack[-1].append((self.block_number, Type))

    def addIterateJunc1(self, Type='flow'):
        self.iterate_junction_stack[-1].append((self.block_number + 1, Type))

    def addIterate(self, Type='flow'):
        self.iterate_stack.append((self.block_number, Type))

    def addIterate_d(self, type='flow'):
        self.iterate_stack_d.append((self.block_number, type))

    def addSwitchEdge(self):
        source_node, Type = self.switch_stack[-1]
        dest_node = self.block_number
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addSwitchJunctionEdges(self):
        for source_node, Type in self.switch_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def add_throwedges(self):
        for source_node, Type in self.throw_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def add_throw(self, Type='Exception'):
        self.throw_stack.append((self.block_number, Type))

    def addSwitch(self, Type='switch'):
        self.switch_stack.append((self.block_number, Type))

    def addSwitchJunc(self, Type='flow'):
        self.switch_junction_stack[-1].append((self.block_number, Type))

    def addGotoEdge(self, label):
        source_node = self.block_number
        dest_node = self.label_dict[label]
        self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, 'goto'))
        self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def insertAfter(self, ctx):
        new_code = '\n' + self.logLine() + ';\n'
        self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex, new_code)

    def logLine(self):
        return 'logFile << "' + str(self.domain_name) + ' ' + str(self.block_number) + '" << std::endl'

    def addTryJunc(self, Type='flow'):
        self.try_junction_stack[-1].append((self.block_number, Type))

    def addTryEdges(self):
        for source_node, Type in self.try_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def addTryJuncEdges(self):
        for source_node, Type in self.try_junction_stack[-1]:
            dest_node = self.block_number
            self.block_dict[self.domain_name]["Edges"].append((source_node, dest_node, Type))
            self.CFG_file.write(str(source_node) + ' ' + str(dest_node) + '\n')

    def __init__(self, common_token_stream: CommonTokenStream, number_of_tokens, directory_name, graph_status, cutt):
        """
        :param common_token_stream:
        """
        self.cfg_path = 'CFGS/' + directory_name + '/'
        self.instrument_path = 'Instrument/' + directory_name + '/'
        self.block_dict = {}
        self.block_dict_tokens = {}
        self.block_number = 0
        self.cut_off_status = cutt
        self.token_stream = common_token_stream
        self.graph_status = graph_status
        self.block_start = 0
        self.block_stop = 0
        self.block_tstart = 0
        self.block_tstop = 0
        self.domain_name = 0
        self.function_dict = {}
        self.for_steps = []
        self.select_junction_stack = []
        self.select_decision_stack = []
        self.iterate_junction_stack = []
        self.iterate_stack = []
        self.iterate_stack_d = []
        self.switch_junction_stack = []
        self.temp = []
        self.switch_stack = []
        self.switch_for_stack = []
        self.has_jump_stack = []
        self.is_for = []
        self.is_while = []
        self.is_doWhile = []
        self.is_rfor = []
        self.rfor_declarator = []
        self.has_default_stack = []
        self.has_case_stack = []
        self.try_stack = []
        self.try_junction_stack = []
        self.is_catch = False
        self.throw_stack = []
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

    # function
    def enterFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):
        self.initial_nodes = set()
        self.final_nodes = set()
        temp = ctx.declarator().getText().replace('~', "destructor")
        function_name = ''.join(c for c in temp if c.isalnum())
        self.domain_name += 1
        self.function_dict[self.domain_name] = (function_name, ctx.start.line)
        self.block_dict[self.domain_name] = {
            "Nodes": [],
            "Edges": []
        }
        self.block_dict_tokens[self.domain_name] = {"Nodes": []}
        self.CFG_file = open(self.cfg_path + str(self.domain_name) + '.txt', 'w')

    def block_cutoff(self):
        tmp = self.token_stream.getText(self.block_tstart, self.block_tstop)
        return ((tmp))

    def enterFunctionbody1(self, ctx: CPP14_v2Parser.Functionbody1Context):  # normal function
        self.block_number = 1
        self.block_start = ctx.start.line

        self.block_tstart = ctx.start.tokenIndex
        self.has_jump_stack.append(False)
        self.insertAfter(ctx)
        self.initial_nodes.add(self.block_number)

    def enterCompoundstatement(self, ctx: CPP14_v2Parser.CompoundstatementContext):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Functionbody1Context):
            pass

    def enterStatementseq2(self, ctx: CPP14_v2Parser.Statementseq2Context):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.CompoundstatementContext):
            pass

    def enterFunctiontryblock(self, ctx: CPP14_v2Parser.FunctiontryblockContext):  # try function
        self.block_number = 1
        self.block_start = ctx.start.line

        self.block_tstart = ctx.start.tokenIndex
        self.has_jump_stack.append(False)
        body = ctx.compoundstatement()
        self.insertAfter(body)
        self.initial_nodes.add(self.block_number)
        self.try_stack.append(set())
        self.try_junction_stack.append(list())

    def enterTryblock(self, ctx: CPP14_v2Parser.TryblockContext):
        self.is_catch = True
        self.block_stop = ctx.start.line
        self.block_tstop = ctx.start.tokenIndex

        self.addNode()

        self.addInitEdge()
        self.is_catch = True
        self.has_jump_stack.append(False)
        self.try_stack.append(set())
        self.try_junction_stack.append(list())
        self.block_number += 1
        self.block_start = ctx.start.line + 1
        self.block_tstart = ctx.start.tokenIndex + 1
        body = ctx.compoundstatement()
        self.insertAfter(body)

    def exitCompoundstatement(self, ctx: CPP14_v2Parser.CompoundstatementContext):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.TryblockContext):
            self.is_catch = True

            self.has_jump_stack.pop() + 1
            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex
            self.addNode()
            self.addTryJunc()


        elif isinstance(ctx.parentCtx, CPP14_v2Parser.FunctiontryblockContext):
            self.is_catch = True

            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex
            self.addNode()

    def enterHandler(self, ctx: CPP14_v2Parser.HandlerContext):
        self.is_catch = True
        self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex
        body = ctx.compoundstatement()
        self.insertAfter(body)
        self.addTryEdges()
        self.has_jump_stack.append(False)

    def exitHandler(self, ctx: CPP14_v2Parser.HandlerContext):
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        self.addTryJunc()

        self.has_jump_stack.pop()

    def exitTryblock(self, ctx: CPP14_v2Parser.TryblockContext):

        self.is_catch = True
        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1
        self.addTryJuncEdges()
        self.try_junction_stack.pop()
        self.try_stack.pop()
        self.is_catch = True

        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitFunctiontryblock(self, ctx: CPP14_v2Parser.FunctiontryblockContext):

        self.is_catch = True
        self.try_stack.pop()

    # selection

    def enterSelectionstatement1(self, ctx: CPP14_v2Parser.Selectionstatement1Context):  # if

        pass

    def enterForrangedeclaration(self, ctx: CPP14_v2Parser.ForrangedeclarationContext):
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()

    def enterStatement(self, ctx: CPP14_v2Parser.StatementContext):
        """
        DFS traversal of a statement subtree, rooted at ctx.
        If the statement is a branching condition insert a prob.
        :param ctx:
        :return:
        """
        # do-while and range-for
        # line 342(CPP14_v2Parser.Iterationstatement4Context)
        # if isinstance(ctx.children ,(CPP14_v2Parser.ExpressionstatementContext)):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Iterationstatement4Context):
            pass
        if isinstance(ctx.parentCtx,
                      (CPP14_v2Parser.Iterationstatement2Context)):


            body = ctx.compoundstatement()
            if body != None:
                self.insertAfter(body)
            # if there is only one statement after the branchning condition then create a block.
            else:
                new_code = '{'
                new_code += '\n' + self.logLine() + ';\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
            return
        # one line while and for
        elif isinstance(ctx.parentCtx, CPP14_v2Parser.IterationstatementContext):
            self.block_number += 1

            self.block_start = ctx.start.line

            self.block_tstart = ctx.start.tokenIndex
            # if there is a compound statement after the branchning condition:
            body = ctx.compoundstatement()
            if body != None:
                self.insertAfter(body)
            # if there is only one statement after the branchning condition then create a block.
            else:
                new_code = '{'
                new_code += '\n' + self.logLine() + ';\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
        elif isinstance(ctx.parentCtx,
                        (CPP14_v2Parser.Selectionstatement1Context, CPP14_v2Parser.Selectionstatement2Context)):

            self.block_number += 1

            self.block_start = ctx.start.line

            self.block_tstart = ctx.start.tokenIndex

            self.addDecisionEdge()

            self.has_jump_stack.append(False)

            # if there is a compound statement after the branchning condition:
            body = ctx.compoundstatement()
            if body != None:
                self.insertAfter(body)
            # if there is only one statement after the branchning condition then create a block.
            else:
                new_code = '{'
                new_code += '\n' + self.logLine() + ';\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)

        elif isinstance(ctx.parentCtx,
                        CPP14_v2Parser.Selectionstatement3Context):
            if ctx.compoundstatement() == None:
                new_code = '{\n'
                self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)

    def extract_exact_text(self, rule: ParserRuleContext) -> str:
        return self.token_stream.getText(rule.start.tokenIndex, rule.stop.tokenIndex)

    def exitStatement(self, ctx: CPP14_v2Parser.StatementContext):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.IterationstatementContext):  # loop

            if self.is_for.pop():
                self.addInitEdge("flow")

                self.block_stop = ctx.stop.line

                self.block_tstop = ctx.stop.tokenIndex
                self.addNode()
                self.block_number += 1
                self.block_stop = self.for_steps.pop()
                self.block_start = self.for_steps.pop()
                self.block_tstop = self.for_steps.pop()
                self.block_tstart = self.for_steps.pop()
                self.addNode()
                self.addIterateEdge()

            if self.is_while.pop():
                self.addIterateEdge()
                self.block_stop = ctx.stop.line
                self.block_tstop = ctx.stop.tokenIndex
                self.addNode()

            if self.is_rfor.pop():
                # pass
                self.addInitEdge("flow")

                self.block_stop = ctx.stop.line
                self.block_tstop = ctx.stop.tokenIndex
                self.addNode()
                self.block_number += 1
                self.block_stop = self.rfor_declarator.pop()
                self.block_start = self.rfor_declarator.pop()
                self.block_tstop = self.rfor_declarator.pop()
                self.block_tstart = self.rfor_declarator.pop()
                self.addNode()
                self.addIterateEdge()


            if ctx.compoundstatement() == None:
                new_code = '\n}'
                self.afterInsert[ctx.stop.tokenIndex] += new_code


        elif isinstance(ctx.parentCtx,
                        (CPP14_v2Parser.Selectionstatement1Context, CPP14_v2Parser.Selectionstatement2Context)):  # if
            if (ctx.getText()[0:2] == "if"):
                self.block_number -= 1
                return

            self.block_stop = ctx.stop.line

            self.block_tstop = ctx.stop.tokenIndex
            self.addNode()

            if not self.has_jump_stack.pop():

                self.addJunc()

            if ctx.compoundstatement() == None:
                new_code = '\n}'
                self.afterInsert[ctx.stop.tokenIndex] += new_code

        elif isinstance(ctx.parentCtx,
                        CPP14_v2Parser.Selectionstatement3Context):  # switch
            if ctx.compoundstatement() == None:
                new_code = '\n}'
                self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitSelectionstatement1(self, ctx: CPP14_v2Parser.Selectionstatement1Context):  # if

        self.block_number += 1

        self.block_start = ctx.stop.line + 1

        self.block_tstart = ctx.stop.tokenIndex + 1

        self.addJunctionEdges()

        self.select_junction_stack.pop()

        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def enterSelectionstatement2(self, ctx: CPP14_v2Parser.Selectionstatement2Context):  # if-else
        pass

    def enterSelectionstatement3(self, ctx: CPP14_v2Parser.Selectionstatement3Context):  # switch
        self.block_stop = ctx.start.line
        self.block_tstop = ctx.start.tokenIndex + 4
        self.addNode()
        self.addSwitch()
        self.has_jump_stack.append(True)
        self.has_default_stack.append(False)
        self.has_case_stack.append(False)
        self.switch_for_stack.append(SWITCH_FOR["switch"])
        self.switch_junction_stack.append(list())

    def enterLabeledstatement1(self, ctx: CPP14_v2Parser.Labeledstatement1Context):  # label
        try:
            if not self.has_jump_stack[-1]:
                self.addInitEdge()
                self.block_stop = ctx.start.line
                self.block_tstop = ctx.start.tokenIndex
                self.addNode()
        except:
            self.addInitEdge()
            self.block_stop = ctx.start.line
            self.block_tstop = ctx.start.tokenIndex
            self.addNode()
        self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex
        label = ctx.Identifier().getText()
        self.label_dict[label] = self.block_number
        try:
            for source_node in self.goto_dict[label]:
                self.block_dict[self.domain_name]["Edges"].append((source_node, self.block_number))
                self.CFG_file.write(str(source_node) + ' ' + str(self.block_number) + '\n')
        except:
            pass
        index = ctx.statement().start.tokenIndex
        new_code = self.logLine() + ';\n'
        self.token_stream_rewriter.insertBeforeIndex(index, new_code)

    def enterLabeledstatement2(self, ctx: CPP14_v2Parser.Labeledstatement2Context):  # case
        self.block_stop = ctx.start.line - 1
        self.block_tstop = ctx.start.tokenIndex - 1
        self.addNode()
        try:
            if not self.has_jump_stack.pop():
                self.addInitEdge()
        except:
            pass
        self.has_case_stack[-1] = True
        self.has_jump_stack.append(False)
        self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex
        if not self.has_default_stack[-1]:
            self.addSwitchEdge()
        index = ctx.statement().start.tokenIndex
        new_code = self.logLine() + ';\n'
        self.token_stream_rewriter.insertBeforeIndex(index, new_code)

    def enterLabeledstatement3(self, ctx: CPP14_v2Parser.Labeledstatement3Context):  # default
        self.block_stop = ctx.start.line
        self.block_tstop = ctx.start.tokenIndex
        self.addNode()
        try:
            if not self.has_jump_stack.pop():
                self.addInitEdge()
        except:
            pass
        self.has_default_stack[-1] = True
        self.has_jump_stack.append(False)
        self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex
        self.addSwitchEdge()
        index = ctx.statement().start.tokenIndex
        new_code = self.logLine() + ';\n'
        self.token_stream_rewriter.insertBeforeIndex(index, new_code)

    # iteration
    def enterIterationstatement1(self, ctx: CPP14_v2Parser.Iterationstatement1Context):  # while
        self.switch_for_stack.append(SWITCH_FOR["for_while"])
        self.has_jump_stack.append(False)
        self.is_for.append(False)
        self.is_while.append(True)
        self.is_rfor.append(False)
        self.is_doWhile.append(False)
        self.block_stop = ctx.start.line - 1
        self.block_tstop = ctx.start.tokenIndex - 1
        self.addNode()
        self.addInitEdge()
        """self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex +1
        self.block_stop = self.block_start
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()"""

    def enterIterationstatement3(self, ctx: CPP14_v2Parser.Iterationstatement3Context):  # for
        self.switch_for_stack.append(SWITCH_FOR["for_while"])
        self.has_jump_stack.append(False)
        self.is_for.append(True)
        self.is_while.append(False)
        self.is_doWhile.append(False)
        self.is_rfor.append(False)
        # self.block_stop = ctx.start.line
        # self.block_tstop = ctx.start.tokenIndex
        # self.addNode()

        """self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex+1
        self.block_stop = self.block_start
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()"""

        if ctx.condition() == None:
            new_code = self.logLine() + ' '
            self.token_stream_rewriter.insertAfter(ctx.forinitstatement().stop.tokenIndex, new_code)

    def enterIterationstatement2(self, ctx: CPP14_v2Parser.Iterationstatement2Context):  # do-while
        self.switch_for_stack.append(SWITCH_FOR["for_while"])
        self.has_jump_stack.append(False)
        self.is_while.append(False)
        self.is_for.append(False)
        self.is_rfor.append(False)
        self.is_doWhile.append(True)
        self.iterate_junction_stack.append(list())

        self.block_stop = ctx.start.line - 1
        self.block_tstop = ctx.start.tokenIndex - 1
        self.addNode()
        self.temp.append(self.block_number)
        self.addInitEdge()
        self.addIterate_d("True")

        self.block_number += 1

        self.block_start = ctx.start.line

        self.block_tstart = ctx.start.tokenIndex - 1

        self.addIterate("True")
        expression = ctx.expression()

        new_code = self.logLine()
        new_code += ' && ('
        self.token_stream_rewriter.insertBeforeIndex(expression.start.tokenIndex, new_code)
        new_code = ')'
        self.token_stream_rewriter.insertAfter(expression.stop.tokenIndex, new_code)

        """self.block_number += 1
        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex+1"""

    def enterIterationstatement4(self, ctx: CPP14_v2Parser.Iterationstatement4Context):  # range-for
        self.switch_for_stack.append(SWITCH_FOR["range_for"])
        self.has_jump_stack.append(False)
        self.is_for.append(False)
        self.is_while.append(False)
        self.is_doWhile.append(False)
        self.is_rfor.append(True)
        """self.block_stop = ctx.start.line
        self.block_tstop = ctx.start.tokenIndex
        self.addNode()"""
        self.addInitEdge("flow")

        self.iterate_junction_stack.append(list())

        """if ctx.condition() == None:
            new_code = self.logLine() + ' '
            self.token_stream_rewriter.insertAfter(ctx.forinitstatement().stop.tokenIndex, new_code)"""

    def enterExpression(self, ctx: CPP14_v2Parser.ExpressionContext):
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Iterationstatement2Context):
            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex + 1
            self.addNode()
            self.addIterateEdge_dwhile()
            self.addIterateJunc("False")

        if isinstance(ctx.parentCtx, CPP14_v2Parser.Iterationstatement3Context):
            self.for_steps.append(ctx.start.tokenIndex)
            self.for_steps.append(ctx.stop.tokenIndex)
            self.for_steps.append(ctx.start.line)
            self.for_steps.append(ctx.stop.line)

    def enterCondition(self, ctx: CPP14_v2Parser.ConditionContext):  # for and while and if condition
        if not isinstance(ctx.parentCtx, CPP14_v2Parser.Selectionstatement3Context):
            new_code = self.logLine()
            new_code += ' && ('
            self.token_stream_rewriter.insertBeforeIndex(ctx.start.tokenIndex, new_code)
            new_code = ')'
            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Iterationstatement3Context):
            self.block_number += 1

            self.block_start = ctx.start.line
            self.block_tstart = ctx.start.tokenIndex

            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex
            self.addNode()
            self.addIterateJunc('False')
            self.addIterate()
            self.addInitEdge('True')
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Iterationstatement1Context):
            self.block_number += 1

            self.block_start = ctx.start.line
            self.block_tstart = ctx.start.tokenIndex - 2

            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex + 1
            self.addNode()
            self.iterate_junction_stack.append(list())
            self.addIterateJunc('False')
            self.addIterate()
            self.addInitEdge('True')
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Selectionstatement1Context):
            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex + 1
            self.addNode()

            self.select_junction_stack.append(list())
            # self.addInitEdge()

            self.addDecision('True')

            self.addJunc('False')
        if isinstance(ctx.parentCtx, CPP14_v2Parser.Selectionstatement2Context):
            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex + 1
            self.addNode()
            self.select_junction_stack.append(list())

            self.addDecision('False')
            self.addDecision('True')

    def enterForinitstatement2(self, ctx: CPP14_v2Parser.Forinitstatement2Context):
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        self.addInitEdge("flow")

        self.iterate_junction_stack.append(list())

    def enterForrangeinitializer1(self, ctx: CPP14_v2Parser.Forrangeinitializer1Context):
        self.block_number += 1

        self.block_start = ctx.start.line
        self.block_tstart = ctx.start.tokenIndex

        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        self.addIterateJunc('False')
        self.addIterate()
        self.addInitEdge('True')
        self.rfor_declarator.append(ctx.start.tokenIndex)
        self.rfor_declarator.append(ctx.stop.tokenIndex)
        self.rfor_declarator.append(ctx.start.line)
        self.rfor_declarator.append(ctx.stop.line)

    def exitSelectionstatement2(self, ctx: CPP14_v2Parser.Selectionstatement2Context):  # if-else

        self.block_number += 1

        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1

        self.addJunctionEdges()
        self.select_junction_stack.pop()
        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitSelectionstatement3(self, ctx: CPP14_v2Parser.Selectionstatement3Context):  # switch
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        self.switch_for_stack.pop()
        if not self.has_default_stack.pop():
            self.switch_junction_stack[-1].append((self.switch_stack.pop()[0], 'not match'))
            if not self.has_case_stack.pop():
                self.has_jump_stack.pop()
            elif not self.has_jump_stack.pop():
                self.addSwitchJunc()
        elif not self.has_jump_stack.pop():
            self.addSwitchJunc()

        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1
        self.addSwitchJunctionEdges()
        self.switch_junction_stack.pop()
        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitIterationstatement1(self, ctx: CPP14_v2Parser.Iterationstatement1Context):  # while
        self.iterate_stack.pop()
        self.switch_for_stack.pop()
        self.has_jump_stack.pop()
        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1
        self.addIterateJunctionEdges()
        self.iterate_junction_stack.pop()
        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitIterationstatement3(self, ctx: CPP14_v2Parser.Iterationstatement3Context):  # for

        self.iterate_stack.pop()
        self.switch_for_stack.pop()
        self.has_jump_stack.pop()
        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1

        self.addIterateJunctionEdges()
        self.iterate_junction_stack.pop()

        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitIterationstatement2(self, ctx: CPP14_v2Parser.Iterationstatement2Context):  # do-while
        self.iterate_stack.pop()
        self.switch_for_stack.pop()
        self.has_jump_stack.pop()
        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1
        self.addIterateJunctionEdges()

        self.iterate_junction_stack.pop()

        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitIterationstatement4(self, ctx: CPP14_v2Parser.Iterationstatement4Context):  # range-for
        self.iterate_stack.pop()
        self.switch_for_stack.pop()
        self.has_jump_stack.pop()
        self.block_number += 1
        self.block_start = ctx.stop.line + 1
        self.block_tstart = ctx.stop.tokenIndex + 1
        self.addIterateJunctionEdges()
        self.iterate_junction_stack.pop()
        new_code = '\n' + self.logLine() + ';\n'
        self.afterInsert[ctx.stop.tokenIndex] += new_code

    def exitFunctionbody1(self, ctx: CPP14_v2Parser.Functionbody1Context):
        """
         Insert a prob at the end of the function only if the function is void.
        :param ctx:
        :return:
        """
        if not self.has_jump_stack.pop():
            self.block_stop = ctx.stop.line
            self.block_tstop = ctx.stop.tokenIndex
            self.addNode()
            self.final_nodes.add(self.block_number)

    def enterJumpstatement1(self, ctx: CPP14_v2Parser.Jumpstatement1Context):  # break
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        try:
            self.has_jump_stack[-1] = True
        except:
            pass
        if self.switch_for_stack[-1] == SWITCH_FOR["switch"]:
            self.addSwitchJunc()
        else:
            self.addIterateJunc()

    def enterJumpstatement2(self, ctx: CPP14_v2Parser.Jumpstatement2Context):  # continue
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        try:
            self.has_jump_stack[-1] = True
        except:
            pass
        i = 1
        while (self.switch_for_stack[-i] == SWITCH_FOR["switch"]):
            i = i - 1
        if self.switch_for_stack[-i] == SWITCH_FOR["range_for"]:
            self.addIterateJunc()
        self.addIterateEdge()

    def enterJumpstatement3(self, ctx: CPP14_v2Parser.Jumpstatement3Context):  # return
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()

        try:
            self.has_jump_stack[-1] = True
        except:
            pass
        self.final_nodes.add(self.block_number)

    def enterJumpstatement4(self, ctx: CPP14_v2Parser.Jumpstatement4Context):  # return
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        try:
            self.has_jump_stack[-1] = True
        except:
            pass
        self.final_nodes.add(self.block_number)

    def enterJumpstatement5(self, ctx: CPP14_v2Parser.Jumpstatement5Context):  # goto
        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex
        self.addNode()
        try:
            self.has_jump_stack[-1] = True
        except:
            pass
        label = ctx.Identifier().getText()
        try:
            self.addGotoEdge(label)
        except:
            try:
                self.goto_dict[label] += [self.block_number]
            except:
                self.goto_dict[label] = [self.block_number]

    def enterThrowexpression(self, ctx: CPP14_v2Parser.ThrowexpressionContext):  # throw
        self.is_catch = False

        self.block_stop = ctx.stop.line
        self.block_tstop = ctx.stop.tokenIndex

        self.addNode()

        try:
            self.has_jump_stack[-1] = True
        except:
            pass

        self.is_catch = True

    def cutoff_func(self):
        deleted_block = []
        for tm in self.block_dict_tokens[self.domain_name]["Nodes"]:
            tmp = self.token_stream.getText(tm[1], tm[2])
            if (tmp.strip() == "}" or tmp.strip() == ""):
                deleted_block.append(tm[0] - 1)
        cnt = 0
        for i in deleted_block:
            self.block_dict_tokens[self.domain_name]["Nodes"].pop(i - cnt)
            self.block_dict[self.domain_name]["Nodes"].pop(i - cnt)
            cnt += 1

        for tm in self.block_dict_tokens[self.domain_name]["Nodes"]:
            (self.block_dict_tokens[self.domain_name]["Nodes"].index(tm))

        next_block = []
        # test = []
        for a in range(len(deleted_block)):
            deleted_block[a] += 1
        for x in self.block_dict[self.domain_name]["Edges"]:
            for y in deleted_block:
                if (x[0] == y and x[2] == "flow"):
                    # print(x[0],y)
                    # test.append(x[0])
                    # test.append(x[1])
                    # print("hi")
                    next_block.append([x[0], x[1]])
                    te = int(self.block_dict[self.domain_name]["Edges"].index(x))
                    # print(type(te))
                    self.block_dict[self.domain_name]["Edges"].pop(te)

                # if(x[1]==y):
                # print(x)
        # print(next_block)
        for it in self.block_dict[self.domain_name]["Edges"]:

            for a, s in next_block:
                # print(a,s)
                if (it[1] == a):
                    te = (self.block_dict[self.domain_name]["Edges"].index(it))
                    # print(self.block_dict[self.domain_name]["Edges"][te],"its",s)
                    # print(a,type(a))
                    self.block_dict[self.domain_name]["Edges"].insert(te, (it[0], s, it[2]))
                    te = int(self.block_dict[self.domain_name]["Edges"].index(it))

                    self.block_dict[self.domain_name]["Edges"].pop(te)

        edited_num = []
        for x in self.block_dict[self.domain_name]["Nodes"]:
            te = (self.block_dict[self.domain_name]["Nodes"].index(x))
            if (x[0] != te + 1):
                tp = te + 1
                edited_num.append([x[0], tp])
                (self.block_dict[self.domain_name]["Nodes"].insert(te, [tp, x[1], x[2]]))
                te = (self.block_dict[self.domain_name]["Nodes"].index(x))
                self.block_dict[self.domain_name]["Nodes"].pop(te)

        for x in self.block_dict_tokens[self.domain_name]["Nodes"]:
            te = (self.block_dict_tokens[self.domain_name]["Nodes"].index(x))
            if (x[0] != te + 1):
                tp = te + 1
                # edited_num.append([x[0],tp])
                (self.block_dict_tokens[self.domain_name]["Nodes"].insert(te, [tp, x[1], x[2]]))
                te = (self.block_dict_tokens[self.domain_name]["Nodes"].index(x))
                self.block_dict_tokens[self.domain_name]["Nodes"].pop(te)

        tb_pop = []

        # breakpoint()
        for x in self.block_dict[self.domain_name]["Edges"]:

            for s, e in edited_num:
                if (x[0] == s):
                    te = (self.block_dict[self.domain_name]["Edges"].index(x))
                    tb_pop.append(x)
                    # print(x)
                    self.block_dict[self.domain_name]["Edges"].insert(te, (e, x[1], x[2]))
                    te = (self.block_dict[self.domain_name]["Edges"].index(x))
                    self.block_dict[self.domain_name]["Edges"].pop(te)
        # breakpoint()
        for x in self.block_dict[self.domain_name]["Edges"]:
            # print(x)
            for s, e in edited_num:
                if (x[1] == s):
                    te = (self.block_dict[self.domain_name]["Edges"].index(x))
                    tb_pop.append(x)
                    # print(x)
                    self.block_dict[self.domain_name]["Edges"].insert(te, (x[0], e, x[2]))
                    te = (self.block_dict[self.domain_name]["Edges"].index(x))
                    self.block_dict[self.domain_name]["Edges"].pop(te)

    def exitFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):
        initial_nodes_str = ' '.join(str(node) for node in self.initial_nodes)
        self.CFG_file.write("initial nodes:" + initial_nodes_str + '\n')
        self.final_nodes.add(self.block_number)
        final_nodes_str = ' '.join(str(node) for node in self.final_nodes)
        self.CFG_file.write("final nodes:" + final_nodes_str + '\n')

        graph_json = open(self.cfg_path + str(self.domain_name) + '.json', 'w')
        json.dump(self.block_dict[self.domain_name], graph_json)
        json.dump(self.block_dict_tokens[self.domain_name], graph_json)

        self.CFG_file.close()
        temp = []
        token_numbers = []
        line_numbers = []
        func_graph = nx.DiGraph()
        func_graph.add_nodes_from([(str(n)) for n, s, e in self.block_dict[self.domain_name]["Nodes"]])
        func_graph.add_edges_from([(str(s), str(d)) for s, d, T in self.block_dict[self.domain_name]["Edges"]])
        temp.append([(str(s), str(d), str(T)) for s, d, T in self.block_dict[self.domain_name]["Edges"]])

        token_numbers = [(s, e) for n, s, e in self.block_dict_tokens[self.domain_name]["Nodes"]]
        line_numbers = [(s, e) for n, s, e in self.block_dict[self.domain_name]["Nodes"]]

        Nodes_list = [*func_graph.nodes]
        edge_labels = {}
        f_nodes = []
        for s, d, T in self.block_dict[self.domain_name]["Edges"]:
            edge_labels[(s, d)] = T
        graph = gv.Digraph(node_attr={'shape': 'none'})
        graph.node('start', style='filled', fillcolor='#92ca38', fontsize='22', shape='ellipse')
        graph.node('end', style='filled', fillcolor='#dc1e78', fontsize='22', shape='ellipse')
        for node in func_graph:
            if func_graph.out_degree(node) == 0:
                f_nodes.append(node)

        for i, token_number, line_number in zip(func_graph, token_numbers, line_numbers):

            if (self.graph_status == 1):
                expres = self.token_stream.getText(int(token_number[0]), int(token_number[1]))
                lines = [html.escape(f"{i + line_number[0]}: {line}") for i, line in enumerate(expres.strip().split("\n"))]
                delimiter = '<br align="left"/>\n'
                expres = delimiter.join(lines) + delimiter
            else:
                expres = (line_number[0]) + "-" + (line_number[1])

            graph.node(str(Nodes_list[int(i) - 1]), label=f'''<
<FONT POINT-SIZE="22">
               <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <tr>
                         <td width="30" height="30" fixedsize="true">{i}</td>
                         <td width="9" height="9" fixedsize="true" style="invis"></td>
                         <td width="9" height="9" fixedsize="true" style="invis"></td>
                    </tr>
                    <tr>
                         <td width="30" height="40" fixedsize="false" sides="tlb"></td>
                         <td width="50" height="40" fixedsize="false" sides="bt">{(str(expres))}</td>
                         <td width="30" height="40" fixedsize="false" sides="brt"></td>
                    </tr>
            </TABLE>
            </FONT>>''')

        for items in f_nodes:
            graph.edge(f'{str(Nodes_list[int(items) - 1])}', 'end')

        for x in temp[0]:
            if (x[0] <= x[1]):
                graph.edge(f'{x[0]}', f'{x[1]}', x[2], fontsize='22')
            else:
                graph.edge(f'{x[0]}', x[1], x[2], fontsize='22')
        graph.edge('start', f'{str(Nodes_list[0])}')

        graph.render(f'{self.cfg_path}/{str(self.domain_name)}.gv', view=True)

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
