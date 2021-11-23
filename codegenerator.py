from constants import *


class CodeGenerator:
    def __init__(self):
        self.tokens = []
        self.flag = False
        self.count_of_t = 1
        self.current_token_index = 0
        self.output = []
        self.errors = []

    def parse(self, tokens: list, errors: list):
        self.tokens = tokens
        self.errors = errors
        if len(tokens) > 1:
            if len(self.errors) != 0:
                self.output.append("There is an error in the syntax of the code")
                return
            while not self.is_current_token_an([LexerToken.END_OF_FILE]):
                self.Start()
            self.output.append("\n\nif __name__ == " + '"__main__":\n    main()\n')
        else:
            self.output.append("Empty file.\n")

    def write_output_to_file(self, filename: str):
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

    def token_is(self, token_to_match: str) -> bool:
        if self.tokens[self.current_token_index].lexeme == token_to_match:
            self.advance_token()
            return True
        else:
            return False

    def token_in(self, token_list: list) -> bool:
        if len(token_list) == 1:
            return self.token_is(token_list[0])
        else:
            if self.tokens[self.current_token_index].lexeme in token_list:
                self.advance_token()
                return True
            else:
                return False

    def is_current_token_an(self, token_types: list) -> bool:
        if self.tokens[self.current_token_index].token in token_types:
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def indentation(self):
        if not self.output[-1] == "):\n":
            self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")

    def Start(self):
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.token_is('('):
                    if not self.output:
                        self.output.append("def " + self.tokens[self.current_token_index-2].lexeme + "(")
                    else:
                        self.output.append("\n\ndef " + self.tokens[self.current_token_index-2].lexeme + "(")
                    if self.Initialization():
                        self.token_is(')')
                        self.token_is('{')
                        while not self.token_is("}"):
                            self.Statement()

    def Statement(self) -> bool:
        start = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.indentation()
            start = self.Assignment()
        elif self.token_in(Constants.VALID_DATA_TYPES):
            self.indentation()
            start = self.Declaration()
        elif self.token_is("if"):
            start = self.If_Statement()
            self.count_of_t -= 1
        elif self.token_is("for"):
            start = self.For_Loop()
            self.count_of_t -= 1
        elif self.token_is("while"):
            start = self.While_Loop()
            self.count_of_t -= 1
        elif self.token_is("return"):
            self.indentation()
            self.output.append("return ")
            start = self.Expression()
            self.token_in(Constants.VALID_EOL_SYMBOLS)

        return start

    # done
    def Declaration(self) -> bool:
        declaration = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if self.Instruction():
                declaration = True

        return declaration

    # done
    def Assignment(self) -> bool:
        assignment = False
        if self.token_is('('):
            self.output.append(self.tokens[self.current_token_index-2].lexeme +
                               self.tokens[self.current_token_index-1].lexeme)
            if self.Function_Parameters():
                if self.token_is(')'):
                    self.output.append(")")
                self.token_in(Constants.VALID_EOL_SYMBOLS)
        elif self.Instruction():
            assignment = True

        return assignment

    # done
    def Initialization(self) -> bool:
        initial = True
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                self.output.append(self.tokens[self.current_token_index-1].lexeme)
                if self.token_is(','):
                    self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
                    self.Initialization()
                else:
                    self.output.append("):\n")
            else:
                initial = False
        else:
            self.output.append("):\n")

        return initial

    # done
    def Instruction(self) -> bool:
        instruction = False
        operator_token = self.tokens[self.current_token_index-1].lexeme
        if self.token_is('='):
            self.output.append(operator_token + " " + self.tokens[
                self.current_token_index - 1].lexeme + " ")
            if self.Expression():
                instruction = True
            if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                instruction = False

        return instruction

    # done
    def If_Statement(self) -> bool:
        ifstate = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.count_of_t += 1
        if self.token_is("("):
            if self.Conditional(False):
                if self.token_is(")"):
                    self.output[-1] = self.output[-1].strip()
                    self.output.append(":")
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            self.Statement()
                        ifstate = self.Else()
        self.flag = False
        return ifstate

    # done
    def Conditional(self, flag: bool) -> bool:
        conditional = False
        if flag:
            self.advance_token()
            self.advance_token()
            if self.token_is("="):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("!"):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("<") or self.token_is(">"):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme + "):")
                    self.advance_token()
                    conditional = True
                else:
                    self.output.append(self.tokens[self.current_token_index].lexeme + "):")
                    self.advance_token()
                    conditional = True
        else:
            if self.Expression():
                operator_token = self.tokens[self.current_token_index].lexeme
                if self.token_is("="):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("!"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("<") or self.token_is(">"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                    else:
                        self.output.append(" ")
                        if self.Expression():
                            conditional = True

        return conditional

    # done
    def Else(self) -> bool:
        if self.token_is("else"):
            self.output.append("\n")
            self.count_of_t -= 1
            for i in range(self.count_of_t):
                self.output.append("\t")
            self.count_of_t += 1
            self.output.append(self.tokens[self.current_token_index-1].lexeme + ":")
            if self.token_is("{"):
                while not self.token_is("}"):
                    self.Statement()
        return True

    # done
    def For_Loop(self) -> bool:
        for_loop = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.count_of_t += 1
        if self.token_is("("):
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.output.append(self.tokens[self.current_token_index].lexeme + " in range(")
                self.advance_token()
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme + ", ")
                    self.advance_token()
                if self.Conditional(True):
                    while not self.token_is("{"):
                        self.advance_token()
                    while not self.token_is("}"):
                        self.Statement()
        self.flag = False
        return for_loop

    # done
    def While_Loop(self) -> bool:
        while_loop = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index-1].lexeme)
        self.count_of_t += 1
        if self.token_is("("):
            self.output.append(self.tokens[self.current_token_index-1].lexeme)
            self.Conditional(False)
            if self.token_is(")"):
                self.output[-1] = self.output[-1].strip()
                self.output.append(self.tokens[self.current_token_index-1].lexeme + ":")
                if self.token_is("{"):
                    while not self.token_is("}"):
                        self.Statement()
        self.flag = False
        return while_loop

    # done
    def Expression(self) -> bool:
        expression = False
        if self.Term():
            if self.Expression_Prime():
                expression = True

        return expression

    # done
    def Expression_Prime(self) -> bool:
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append(" " + operator_token + " ")
            if not self.Term():
                expression_prime = False
            else:
                if not self.Expression_Prime():
                    expression_prime = False

        return expression_prime

    # done
    def Term(self) -> bool:
        term = False
        if self.Factor():
            if self.Term_Prime():
                term = True

        return term

    # done
    def Term_Prime(self) -> bool:
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append(" " + operator_token + " ")
            if not self.Factor():
                term_prime = False
            else:
                if not self.Term_Prime():
                    term_prime = False

        return term_prime

    # done
    def Function_Parameters(self) -> bool:
        function_parameters = True
        if self.Expression():
            if self.token_is(","):
                self.output.append(", ")
                self.Function_Parameters()

        return function_parameters

    # not done
    def Factor(self) -> bool:
        factor = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_in(Constants.SIGNED_OPERATORS):
            self.output.append(operator_token)
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False
        else:
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.BOOLEAN]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.token_is('"') or self.token_is("'"):
                self.output.append(self.tokens[self.current_token_index-1].lexeme +
                                   self.tokens[self.current_token_index].lexeme)
                self.is_current_token_an([LexerToken.STRING])
                if not (self.token_is('"') or self.token_is("'")):
                    factor = False
                else:
                    self.output.append(self.tokens[self.current_token_index-1].lexeme)
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False

        return factor
