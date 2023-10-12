from gen.CPP14_v2Listener import CPP14_v2Listener
from gen.CPP14_v2Parser import CPP14_v2Parser

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter


def check_exist_case(ctx_text):
    try:
        first_character = ctx_text[0]
        second_character = ctx_text[1]
        third_character = ctx_text[2]
        fourth_character = ctx_text[3]
        if first_character == 'c' and second_character == 'a' and third_character == 's' and fourth_character == 'e':
            return True
        else:
            return False

    except:
        return False


def check_children(obj, list_obj):
    for item in list_obj:
        if item.parent_index == obj.index:
            item.increment_depth()
            check_children(item, list_obj)


def check_brothers(obj, list_obj):
    for item in list_obj:
        if obj.parent_index == item.parent_index and obj.depth < item.depth and not check_exist_case(obj.text):
            obj.depth = item.depth


def check_parents(ctx, list_obj):
    temp = ctx
    try:
        while True:
            temp = temp.parentCtx
            is_father = find_father(ctx, temp)
            if is_father:
                obj = Instruction(ctx.start.tokenIndex, temp.start.tokenIndex, ctx.stop.tokenIndex, ctx.getText())
                obj.increment_depth()
                list_obj.append(obj)
                check_brothers(obj, list_obj)
                check_children(obj, list_obj)

                break
    except:
        obj = Instruction(ctx.start.tokenIndex, 0, ctx.stop.tokenIndex, ctx.getText())
        list_obj.append(obj)

    return list_obj


def check_exist_else(text, index_original_text):
    first_character = text[index_original_text]
    second_character = text[index_original_text - 1]
    third_character = text[index_original_text - 2]
    fourth_character = text[index_original_text - 3]
    if first_character == 'e' and second_character == 's' and third_character == 'l' and fourth_character == 'e':
        return True
    else:
        return False


def check_exist_close_bracket(text, index_original_text):
    try:
        if text[index_original_text - 4] == '}':
            return True
        else:
            return False
    except:
        return False


def manage_else(stop_statement_0, start_statement_1, self):
    for else_index in range(stop_statement_0 + 1, start_statement_1):
        obj = Else_instruction(else_index, start_statement_1)
        self.else_list.append(obj)


def check_access_modifier(ctx_text):
    isPublic = False
    isPrivate = False
    isProtected = False

    try:
        first_character = ctx_text[0]
        second_character = ctx_text[1]
        third_character = ctx_text[2]
        fourth_character = ctx_text[3]
        if first_character == 'p' and second_character == 'u' and third_character == 'b' and fourth_character == 'l':
            isPublic = True
        else:
            isPublic = False

        if first_character == 'p' and second_character == 'r' and third_character == 'i' and fourth_character == 'v':
            isPrivate = True
        else:
            isPrivate = False

        if first_character == 'p' and second_character == 'r' and third_character == 'o' and fourth_character == 't':
            isProtected = True
        else:
            isProtected = False

        if not isPublic and not isPrivate and not isProtected:
            return False
        else:
            return True

    except:
        return False


def check_exist_try(text, index_original_text):
    first_character = text[index_original_text]
    second_character = text[index_original_text - 1]
    third_character = text[index_original_text - 2]
    if first_character == 'y' and second_character == 'r' and third_character == 't':
        return True
    else:
        return False


def find_father(ctx, parent):
    ctx_text = ctx.getText()
    parent_text = parent.getText()
    start_ctx_text_index = parent_text.find(ctx_text) - 1
    is_exist_try = check_exist_try(parent_text, start_ctx_text_index)

    if parent_text[start_ctx_text_index] == ")" or is_exist_try:
        return True

    find_bracket = 0
    is_exist_else = check_exist_else(parent_text, start_ctx_text_index)
    is_case = check_exist_case(ctx_text)
    is_access_modifier = check_access_modifier(ctx_text)
    is_exist_close_bracket = check_exist_close_bracket(parent_text, start_ctx_text_index)

    if is_exist_else and not is_exist_close_bracket:
        for i in range(start_ctx_text_index, -1, -1):
            if parent_text[i] == ")":
                return True

    if is_exist_else:
        find_bracket -= 1

    for i in range(start_ctx_text_index, -1, -1):

        if parent_text[i] == "}":
            find_bracket += 1

        if parent_text[i] == ":" and find_bracket == 0 and not is_case and not is_access_modifier:
            return True

        if parent_text[i] == "{":
            if find_bracket == 0:
                return True
            else:
                find_bracket -= 1


def exist_brackets_check(text):
    if text.strip()[0] == '{':
        return True
    else:
        return False


class BeautifyListener(CPP14_v2Listener):

    def __init__(self, common_token_stream: CommonTokenStream = None):

        if common_token_stream is None:
            raise TypeError('common_token_stream is None')

        self.token_stream = common_token_stream
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.counter = 0
        self.instruction_list = []
        self.else_list = []

        self.properties = []

    def exitFunctiondefinition(self, ctx: CPP14_v2Parser.FunctiondefinitionContext):  # function
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitSelectionstatement1(self, ctx: CPP14_v2Parser.Selectionstatement1Context):  # if
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitSimpledeclaration1(self, ctx: CPP14_v2Parser.Simpledeclaration1Context):  # declaration ;
        temp = ctx.parentCtx
        grandpa = temp.parentCtx

        try:
            grandpaText = grandpa.getText().split("(")
            if grandpaText[0] != "for":
                self.instruction_list = check_parents(ctx, self.instruction_list)

        except:
            print("Sorry ! ")

    def exitSelectionstatement2(self, ctx: CPP14_v2Parser.Selectionstatement2Context):  # if else
        self.instruction_list = check_parents(ctx, self.instruction_list)
        manage_else(ctx.statement(0).stop.tokenIndex, ctx.statement(1).start.tokenIndex, self)

    def exitExpressionstatement(self,
                                ctx: CPP14_v2Parser.ExpressionstatementContext):  # assign or op (x++ or cout or ..)

        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitSelectionstatement3(self, ctx: CPP14_v2Parser.Selectionstatement3Context):  # switch
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitLabeledstatement1(self, ctx: CPP14_v2Parser.Labeledstatement1Context):  # Identifier:
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitJumpstatement1(self, ctx: CPP14_v2Parser.Jumpstatement1Context):  # Break
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitLabeledstatement2(self, ctx: CPP14_v2Parser.Labeledstatement2Context):  # Case:
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitLabeledstatement3(self, ctx: CPP14_v2Parser.Labeledstatement3Context):  # default :
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitJumpstatement2(self, ctx: CPP14_v2Parser.Jumpstatement2Context):  # Continue
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitJumpstatement3(self, ctx: CPP14_v2Parser.Jumpstatement3Context):  # Return
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitJumpstatement4(self, ctx: CPP14_v2Parser.Jumpstatement4Context):  # Return bracedinitlist
        self.instruction_list = check_parents(ctx, self.instruction_list)

    # def exitJumpstatement5(self, ctx: CPP14_v2Parser.Jumpstatement5Context):  # Goto
    #     self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitIterationstatement3(self, ctx: CPP14_v2Parser.Iterationstatement3Context):  # For
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitIterationstatement1(self, ctx: CPP14_v2Parser.Iterationstatement1Context):  # While
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitIterationstatement2(self, ctx: CPP14_v2Parser.Iterationstatement2Context):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitIterationstatement4(self, ctx: CPP14_v2Parser.Iterationstatement4Context):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitCompoundstatement(self, ctx: CPP14_v2Parser.CompoundstatementContext):  # { ---- }

        if exist_brackets_check(ctx.getText()):
            self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitClassspecifier(self, ctx: CPP14_v2Parser.ClassspecifierContext):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitMemberspecification1(self, ctx: CPP14_v2Parser.Memberspecification1Context):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitMemberspecification2(self, ctx: CPP14_v2Parser.Memberspecification2Context):
        pass
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitHandlerseq(self, ctx: CPP14_v2Parser.HandlerseqContext):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitTryblock(self, ctx: CPP14_v2Parser.TryblockContext):
        self.instruction_list = check_parents(ctx, self.instruction_list)

    def exitFunctiontryblock(self, ctx: CPP14_v2Parser.FunctiontryblockContext):
        self.instruction_list = check_parents(ctx, self.instruction_list)


class Instruction:
    def __init__(self, index, parent_index, end_index, text):
        self.index = index
        self.end_index = end_index
        self.parent_index = parent_index
        self.depth = 0
        self.text = text
        self.depth_counter = 2

    def increment_depth(self):
        self.depth += self.depth_counter


class Else_instruction:
    def __init__(self, start_index, child_start_index):
        self.start_index = start_index
        self.child_start_index = child_start_index
        self.depth = 0
