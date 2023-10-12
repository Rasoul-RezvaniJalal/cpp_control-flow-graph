
from gen.CFGListener import CFGInstListener
from gen.CPP14_v2Lexer import CPP14_v2Lexer
from gen.CPP14_v2Parser import CPP14_v2Parser
from antlr4 import *
import Beautify as Btf
from pathlib import Path
import os


def read_file(file_name):
    status = input(
        "how do you want to show the graph? 1)content in blocks    2)line numbers in block   || type related number : " + "\n")
    if (status == '1'):
        graph_status = 1
    else:
        graph_status = 2

    input_path = file_name
    test_cases_dir = "D:\CodA-master\CodA-master"


    f = open(input_path, 'r' ,encoding="utf8")
    name = Path(f.name).stem
    cfg_path = 'CFGS/' + name
    instrument_path = 'Instrument/' + name
    try:
        os.mkdir(cfg_path)
    except:
        pass
    try:
        os.mkdir(instrument_path)
    except:
        pass

    print("YOUR data was gathered")
    beautify = input \
        ("do you want to beautify it?       1)Beautify my program       2)skip it      ||type related number" + "\n")
    if(beautify == '1'):
        not_beautified = input_path
        source = Btf.run_beautify(not_beautified)
        # os.remove(input_path)
        fo = open(f"beautified_{name}.cpp" ,"w" ,encoding="utf8")
        fo.write(source)
        fo.close()
    else:

        source = f.read()

    stream = InputStream(source)

    lexer = CPP14_v2Lexer(stream)

    token_stream = CommonTokenStream(lexer)

    parser = CPP14_v2Parser(token_stream)

    pars_tree = parser.translationunit()

    lexer.reset()
    number_of_tokens = len(lexer.getAllTokens())
    # cutt = input("do you want to cut_off graph output?      1)yes-cut it off        2)skip this   'STILL UNRELIABLE     ||type related number" + "\n")
    cutt = '2'
    cfg_listener = CFGInstListener(token_stream , number_of_tokens , name ,graph_status ,cutt)
    walker = ParseTreeWalker()
    walker.walk(cfg_listener, pars_tree)

def read_input():
    status = input(
        "how do you want to show the graph? 1)content in blocks    2)line numbers in block   || type related number : " + "\n")
    if (status == '1'):
        graph_status = 1
    else:
        graph_status = 2


    beautify = input(
        "do you want to beautify it?       1)Beautify my program       2)skip it      ||type related number" + "\n")

    # cutt = input("do you want to cut_off graph output?      1)yes-cut it off        2)skip this   'STILL UNRELIABLE     ||type related number" + "\n")
    cutt = '2'
    print("enter your cpp code :" + "\n")

    stream = StdinStream()

    with open("test.cpp", 'w', buffering=20*(1024**2) ,encoding="utf8") as fop:

        fop.write((str(stream )))

        fop.close()

    name = 'test'
    cfg_path = 'CFGS/' + name
    instrument_path = 'Instrument/' + name
    try:
        os.mkdir(cfg_path)
    except:
        pass
    try:
        os.mkdir(instrument_path)
    except:
        pass


    f = open('test.cpp', 'r' ,encoding="utf8")


    if (beautify == '1'):
        f.close()
        not_beautified = 'test.cpp'
        source = Btf.run_beautify(not_beautified)


        fo = open("Beautified_test.cpp" ,"w" ,encoding="utf8")
        fo.write(source)
        fo.close()

    else:

        source = f.read()


    stream = InputStream(source)
    lexer = CPP14_v2Lexer(stream)

    token_stream = CommonTokenStream(lexer)

    parser = CPP14_v2Parser(token_stream)

    pars_tree = parser.translationunit()

    lexer.reset()
    number_of_tokens = len(lexer.getAllTokens())

    cfg_listener = CFGInstListener(token_stream, number_of_tokens, name ,graph_status ,cutt)
    walker = ParseTreeWalker()
    walker.walk(cfg_listener, pars_tree)


def main():
    read_temp= input ("how do you want to read contents? 1)read from file    2)read from input   || type related number : " + "\n")
    if (read_temp == '1'):
        f_name = input("enter the file path: " +"\n")
        read_file(f_name)
    else:

        read_input()


if __name__ == '__main__':
    main()
