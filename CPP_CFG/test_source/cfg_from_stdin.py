from antlr4 import CommonTokenStream, StdinStream

from src.antlr.gen.CPP14_v2Lexer import CPP14_v2Lexer
from src.antlr.gen.CPP14_v2Parser import CPP14_v2Parser
from src.cfg_extractor.cfg_extractor_visitor import CFGExtractorVisitor
from src.graph.visual import draw_CFG


def extract():
    stream = StdinStream()
    lexer = CPP14_v2Lexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = CPP14_v2Parser(token_stream)
    parse_tree = parser.translationunit()
    cfg_extractor = CFGExtractorVisitor(token_stream)
    cfg_extractor.visit(parse_tree)
    funcs = cfg_extractor.functions
    return funcs, token_stream


def main():
    funcs, token_stream = extract()
    for i, g in enumerate(funcs.values()):
        draw_CFG(g, f"../test_output/temp{i}", token_stream)


if __name__ == '__main__':
    main()
