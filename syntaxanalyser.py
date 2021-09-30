from constants import *


class SyntaxAnalyserRDP:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.output = []
        self.errors = []
        self.warnings = []

    def parse(self, tokens):
        self.tokens = tokens

        while not self.is_current_token_an([LexerToken.END_OF_FILE]):
            self.Statement()
            if self.errors != 0:
                break

    def write_output_to_file(self, filename):
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

        with open('C:\My Files\Python\Compilator\errors.txt', "w") as f:
            f.write("{:<20} {:<24}\n\n".format("ERROR", "INDEX_TOKEN"))
            for error in self.errors:
                f.write("{:<24} {:<24}\n".format(error.type, error.index))

        with open('C:\My Files\Python\Compilator\warnings.txt', "w") as f:
            f.write("{:<20} {:<24}\n\n".format("WARNING", "INDEX_TOKEN"))
            for warning in self.warnings:
                f.write("{:<24} {:<24}\n".format(warning.type, warning.index))

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
            new_listing = Listing(self.tokens[self.current_token_index].token,
                                  self.tokens[self.current_token_index].lexeme)

            self.current_token_index += 1

    def backup(self):
        if self.current_token_index > 0:
            self.current_token_index -= 1

    def Statement(self):
        start = False

        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.output.append("<Statement> -> <Assignment>\n")
            start = self.Assignment()
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
            if self.Assignment():
                declaration = True
        else:
            self.output.append("Error: Not a valid identifier.\n")
            self.errors.append(Error(ErrorTypes.NOT_VALID, self.current_token_index))

        return declaration

    def Assignment(self):
        assignment = False
        self.output.append("<Assignment> -> <Identifier> = <Expression>;\n")

        if self.token_is('='):
            if self.Expression():
                assignment = True
            else:
                self.output.append("Error: Invalid expression.\n")
                self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
        else:
            self.output.append("Error: Missing '='.\n")
            self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))

        if not self.token_in(Constants.VALID_EOL_SYMBOLS):
            self.output.append("Warning: Missing ';' at end of line.\n")
            self.warnings.append(Warning(WarningTypes.MISSING, self.current_token_index))

        return assignment

    def If_Statement(self):
        ifstate = False
        self.output.append("<If-Statement> -> if (<Conditional>) {<Statement>} <Else>\n")
        if self.token_is("("):
            if self.Conditional():
                if self.token_is(")"):
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            self.Statement()
                            if len(self.errors) != 0:
                                break
                        ifstate = self.Else()
                    else:
                        self.output.append("Error: Missing \"{\" keyword in If-Statement.\n")
                        self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))
                else:
                    self.output.append("Error: Missing \")\" keyword in If-Statement.\n")
                    self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))
            else:
                self.output.append("Error: Invalid conditional expression.\n")
                self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
        else:
            self.output.append("Error: Missing \"(\" keyword in If-Statement.\n")
            self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))

        return ifstate

    def Conditional(self):
        conditional = False
        self.output.append("<Conditional> -> <Expression> <Conditional-Operator> <Expression>\n")

        if self.Expression():
            if self.token_is("="):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
                else:
                    self.output.append("Error: Unrecognized conditional operator.\n")
                    self.errors.append(Error(ErrorTypes.NOT_VALID, self.current_token_index))
            if self.token_is("!"):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
                else:
                    self.output.append("Error: Unrecognized conditional operator.\n")
                    self.errors.append(Error(ErrorTypes.NOT_VALID, self.current_token_index))
            if self.token_is("<") or self.token_is(">"):
                if self.token_is("=") or self.is_current_token_an([LexerToken.IDENTIFIER, LexerToken.STRING,
                                                                   LexerToken.INTEGER, LexerToken.REAL,
                                                                   LexerToken.BOOLEAN]):
                    if self.Expression():
                        conditional = True
                else:
                    self.output.append("Error: Unrecognized conditional operator.\n")
                    self.errors.append(Error(ErrorTypes.NOT_VALID, self.current_token_index))

        return conditional

    def Else(self):
        if self.token_is("else"):
            self.output.append("<Else> -> else {<Statement>}\n")
            if self.token_is("{"):
                while not self.token_is("}"):
                    self.Statement()
                    if len(self.errors) != 0:
                        break
            else:
                self.output.append("Error: Missing \"{\" at end of function.\n")
                self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))
        else:
            self.output.append("<Else> -> epsilon\n")
        if not self.token_is(";"):
            self.output.append("Warning: Missing ';' at end of line.\n")
            self.warnings.append(Warning(WarningTypes.MISSING, self.current_token_index))
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
                        self.Statement()
                        if len(self.errors) != 0:
                            break
                    if not self.token_is(";"):
                         self.output.append("Warning: Missing ';' at end of line.\n")
                         self.warnings.append(Warning(WarningTypes.MISSING, self.current_token_index))
                else:
                    ...
            else:
                self.output.append("Error: Invalid data type.\n")
                self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
        else:
            self.output.append("Error: Missing \"(\" at end of function.\n")
            self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))

        return for_loop

    def While_Loop(self):
        while_loop = False
        self.output.append("<While-Loop> -> while (<conditional>) {<Statement>};\n ")
        if self.token_is("("):
            self.Conditional()
            self.token_is(")")
            self.token_is("{")
            while not self.token_is("}"):
                self.Statement()
                if len(self.errors) != 0:
                    break
            if not self.token_is(";"):
                self.output.append("Warning: Missing ';' at end of line.\n")
                self.warnings.append(Warning(WarningTypes.MISSING, self.current_token_index))
        else:
            self.output.append("Error: Missing \"(\" at end of function.\n")
            self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))

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
                self.output.append("Error: Invalid term.\n")
            else:
                if not self.Expression_Prime():
                    expression_prime = False
                    self.output.append("Error: Invalid Expression-Prime.\n")
                    self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
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
                        self.output.append("Error: Missing \")\" at end of function.\n")
                        self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))
                        factor = False
            factor = True
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
                self.output.append("Warning: Missing closing string's separator at end of expression.\n")
                self.warnings.append(Warning(WarningTypes.MISSING, self.current_token_index))
            factor = True
        elif self.token_is("("):
            self.output.append("<Factor> -> (<Expression>)\n")
            if (self.Expression()):
                if self.token_is(")"):
                    factor = True
                else:
                    self.output.append("Error: Missing \")\" at end of expression.\n")
                    self.errors.append(Error(ErrorTypes.MISSING, self.current_token_index))
                    factor = False
            else:
                self.output.append("Error: Invalid expression.\n")
                self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
        elif self.is_current_token_an([LexerToken.NOT_EXISTS]):
            self.output.append(
                "Error: Unrecognized value. Factor must be an integer, float, string, identifier or expression.\n")
            self.errors.append(Error(ErrorTypes.NOT_VALID, self.current_token_index))
            factor = False
        elif self.is_current_token_an([LexerToken.INVALID]):
            self.output.append(
                "Error: Unrecognized value. Factor must be an integer, float, string, identifier or expression.\n")
            self.errors.append(Error(ErrorTypes.INVALID, self.current_token_index))
        return factor
