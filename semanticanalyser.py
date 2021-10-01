from syntaxanalyser import SyntaxAnalyserRDP
from lexer import Lexer
from constants import *

class SemanticAnalyser:
    def __init__(self):
        self.tokens = []
        self.positions = []
        self.attributes = []
        self.output = []
        self.errors = []
        self.ids = set()
        self.current_token_index = 0

    def backup(self, flag):
        if self.current_token_index > 0:
            self.current_token_index -= 1
            if flag == 'lexeme':
                value = self.tokens[self.current_token_index].lexeme
            if flag == 'token':
                value = self.tokens[self.current_token_index].token
            self.advance_token()
            return value


    def write_output_to_file(self, filename):
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

        with open('C:\My Files\Python\Compilator\errors.txt', "w") as f:
            f.write("{:<20} {:<24}\n\n".format("ERROR", "INDEX_TOKEN"))
            for error in self.errors:
                f.write("{:<24} {:<24}\n".format(error.type, error.index))

    def parse(self, tokens, positions, errors):
        self.tokens = tokens
        self.positions = positions
        self.errors = errors

        while not self.is_current_token_an([LexerToken.END_OF_FILE]):
            if len(self.errors) != 0:
                break
            self.Statement()


    def token_is(self, token_to_match):
        if self.tokens[self.current_token_index].lexeme == token_to_match:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def token_in(self, token_list):
        if len(token_list) == 1:
            return self.token_is(token_list[0])
        else:
            if self.tokens[self.current_token_index].lexeme in token_list:
                self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                                   "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
                self.advance_token()
                return True
            else:
                return False

    def is_current_token_an(self, token_types):
        if self.tokens[self.current_token_index].token in token_types:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def Statement(self):
        start = False

        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.output.append("<Statement> -> <Assignment>\n")
            if self.backup('lexeme') in self.ids:
                start = self.Assignment()
            else:
                self.output.append("Error: not initialized a variable.  Row = {} , Position = {}\n".format(
                    self.positions[self.current_token_index - 1]['row'],
                    self.positions[self.current_token_index - 1]['pos']))
                self.errors.append(Error(ErrorTypes.NOT_INITIALIZE, self.current_token_index))
        elif self.token_in(Constants.VALID_DATA_TYPES):
            self.output.append("<Statement> -> <Declaration>\n")
            start = self.Declaration()
        elif self.token_is("if"):
            self.output.append("<Statement> -> <If-Statement>\n")
            start = self.If_Statement()
        elif self.token_is("for"):
            self.output.append("<Statement> -> <For-Loop>\n")
            start = self.For_Loop()
        elif self.token_is("while"):
            self.output.append("<Statement> -> <While-Loop>\n")
            start = self.While_Loop()

        return start

    def Declaration(self):
        declaration = False
        self.output.append("<Declaration> -> <Data-Type> <Assignment>\n")
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if self.backup('lexeme') not in self.ids:
                self.ids.add(self.backup('lexeme'))
                if self.Assignment():
                    declaration = True
            else:
                self.output.append("Error: Reinitializing a variable.  Row = {} , Position = {}\n".format(
                    self.positions[self.current_token_index - 1]['row'],
                    self.positions[self.current_token_index - 1]['pos']))
                self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))

        return declaration

    def Assignment(self):
        assignment = False
        self.output.append("<Assignment> -> <Identifier> = <Expression>;\n")

        if self.token_is('='):
            if self.Expression():
                assignment = True

        self.token_in(Constants.VALID_EOL_SYMBOLS)

        return assignment

    def If_Statement(self):
        ifstate = False
        self.output.append("<If-Statement> -> if (<Conditional>) {<Statement>} <Else>\n")
        if self.token_is("("):
            if self.Conditional():
                if self.token_is(")"):
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            if len(self.errors) != 0:
                                break
                            self.Statement()
                        ifstate = self.Else()

        return ifstate

    def Conditional(self):
        conditional = False
        self.output.append("<Conditional> -> <Expression> <Conditional-Operator> <Expression>\n")

        if self.Expression():
            if self.token_is("="):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
            if self.token_is("!"):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True

            if self.token_is("<") or self.token_is(">"):
                if self.token_is("=") or self.is_current_token_an([LexerToken.IDENTIFIER, LexerToken.STRING,
                                                                   LexerToken.INTEGER, LexerToken.REAL,
                                                                   LexerToken.BOOLEAN]):
                    if self.Expression():
                        conditional = True

        return conditional

    def Else(self):
        if self.token_is("else"):
            self.output.append("<Else> -> else {<Statement>}\n")
            if self.token_is("{"):
                while not self.token_is("}"):
                    if len(self.errors) != 0:
                        break
                    self.Statement()
        else:
            self.output.append("<Else> -> epsilon\n")
        self.token_is(";")

        return True

    def For_Loop(self):
        for_loop = False
        self.output.append("<For-loop> -> for (<Declaration><conditional>;<Declaration>) {<Statement>};\n")
        if self.token_is("("):
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.Declaration()
                self.Conditional()
                if self.token_is(";"):
                    self.Declaration()
                    self.token_is(")")
                    self.token_is("{")
                    while not self.token_is("}"):
                        if len(self.errors) != 0:
                            break
                        self.Statement()
                    self.token_is(";")
        return for_loop

    def While_Loop(self):
        while_loop = False
        self.output.append("<While-Loop> -> while (<conditional>) {<Statement>};\n ")
        if self.token_is("("):
            self.Conditional()
            self.token_is(")")
            self.token_is("{")
            while not self.token_is("}"):
                if len(self.errors) != 0:
                    break
                self.Statement()
            self.token_is(";")

        return while_loop

    def Expression(self):
        expression = False
        self.output.append("<Expression> -> <Term> <Expression-Prime>\n")
        if self.Term():
            if self.Expression_Prime():
                expression = True

        return expression

    def Expression_Prime(self):
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append("<Expression-Prime> -> " + operator_token + " <Term> <Expression-Prime>\n")
            if not self.Term():
                expression_prime = False
            else:
                if not self.Expression_Prime():
                    expression_prime = False
        else:
            self.output.append("<Expression-Prime> -> epsilon\n")

        return expression_prime

    def Term(self):
        term = False

        self.output.append("<Term> -> <Factor> <Term-Prime>\n")
        if self.Factor():
            if self.Term_Prime():
                term = True

        return term

    def Term_Prime(self):
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append("<Term-Prime> -> " + operator_token + " <Factor> <Term-Prime>\n")
            if not self.Factor():
                term_prime = False
            else:
                if not self.Term_Prime():
                    term_prime = False
        else:
            self.output.append("<Term-Prime> -> epsilon\n")
        return term_prime

    def Function_Parameters(self):
        function_parameters = True
        self.output.append("<Function-Parameters> -> <Expression> | <Expression>, <Function-Parameters>\n")
        if self.Expression():
            if self.token_is(","):
                self.Function_Parameters()
        else:
            self.output.append("<Function-Parameters> ->  epsilon\n")
        return function_parameters

    def Factor(self):
        factor = True

        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if not self.token_is('('):
                self.output.append("<Factor> -> <Identifier>\n")
            else:
                self.output.append("<Factor> -> <Identifier>(<Function-Parameters>)\n")
                if not self.token_is(')'):
                    self.Function_Parameters()
                    if not self.token_is(')'):
                        factor = False
        elif self.is_current_token_an([LexerToken.INTEGER]):
            self.output.append("<Factor> -> <Integer>\n")
            factor = True
        elif self.is_current_token_an([LexerToken.REAL]):
            self.output.append("<Factor> -> <Float>\n")
            factor = True
        elif self.is_current_token_an([LexerToken.BOOLEAN]):
            self.output.append("<Factor> -> <Boolean>\n")
            factor = True
        elif self.token_is('"') or self.token_is("'"):
            self.output.append("<Factor> -> <String>\n")
            self.is_current_token_an([LexerToken.STRING])
            if not (self.token_is('"') or self.token_is("'")):
                factor = False
        elif self.token_is("("):
            self.output.append("<Factor> -> (<Expression>)\n")
            if self.Expression():
                if self.token_is(")"):
                    factor = True
                else:
                    factor = False
        elif self.is_current_token_an([LexerToken.NOT_EXISTS]) or self.is_current_token_an([LexerToken.INVALID]):
            factor = False
        return factor