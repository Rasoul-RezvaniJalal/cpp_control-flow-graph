from antlr4 import ParseTreeWalker, CommonTokenStream, InputStream, TerminalNode
import antlr4
import antlr4.tree
from gen.CPP14_v2Lexer import CPP14_v2Lexer
from gen.CPP14_v2Listener import CPP14_v2Listener
from gen.CPP14_v2Parser import CPP14_v2Parser
from gen.BeautifyListener import BeautifyListener
from string import whitespace
import os


def remove_blank_line(text):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    #print("Beautify Code Result : \n ")
    result = "".join([s for s in text.splitlines(True) if s.strip()])
    """print(result)
    f = open(dir_path+"\ beautifyCodeResult.cpp", "w")
    f.write(result)
    f.close()"""
    return result


def elseToken_management_depth(list_obj, self):
    for else_item in self.else_list:
        for instruction_item in list_obj:
            if else_item.child_start_index == instruction_item.index:
                else_item.depth = instruction_item.depth - instruction_item.depth_counter


def beautify_code(list_obj, self):
    end_index_list = []
    start_index_list = []

    elseToken_management_depth(list_obj, self)

    for item in list_obj:
        space = ""
        end_taken = False
        start_taken = False

        for x in range(item.depth):
            space = space + " "

        for i in start_index_list:
            if i == item.index:
                start_taken = True

        if not start_taken:
            self.token_stream_rewriter.insertBeforeIndex(item.index, "\n" + space)
            start_index_list.append(item.index)

        for i in end_index_list:
            if i == item.end_index:
                end_taken = True

        if not end_taken and item.index != item.end_index and item.text[len(item.text) - 1] == "}":
            self.token_stream_rewriter.insertBeforeIndex(item.end_index, "\n" + space)
            end_index_list.append(item.end_index)

    for item in self.else_list:
        space = ""
        for x in range(item.depth):
            space = space + " "
        self.token_stream_rewriter.insertBeforeIndex(item.start_index, "\n" + space)


def run_beautify(path):
    file = open(path, "r")
    p1 = file.read()

    print(""
          "Please Wait ...")

    lexer = CPP14_v2Lexer(InputStream(p1))
    tokens = CommonTokenStream(lexer)
    parser = CPP14_v2Parser(tokens)
    parser.getTokenStream()
    tree = parser.translationunit()
    my_listener = BeautifyListener(common_token_stream=tokens)
    walker = ParseTreeWalker()
    walker.walk(t=tree, listener=my_listener)
    beautify_code(my_listener.instruction_list, my_listener)
    rtn = remove_blank_line(my_listener.token_stream_rewriter.getDefaultText())
    return rtn

if __name__ == '__main__':
    input_path = input("please enter the source code path to beautify it :\n")
    run_beautify(input_path)

    #run_beautify("F:\C++\hello.cpp")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
