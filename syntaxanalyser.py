from constants import *


class SyntaxAnalyserRDP:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.output = []

    def parse(self, tokens):
        self.tokens = tokens

        while not self.is_current_token_an(LexerToken.END_OF_FILE):
            self.Statement()

    def write_output_to_file(self, filename):
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

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

    def is_current_token_an(self, token_type):
        if self.tokens[self.current_token_index].token == token_type:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def backup(self):
        if self.current_token_index > 0:
            self.current_token_index -= 1

    def Statement(self):
        start = False

        if self.is_current_token_an(LexerToken.IDENTIFIER):
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

        if self.is_current_token_an(LexerToken.IDENTIFIER):
            if self.Assignment():
                declaration = True
        else:
            self.output.append("Error: Not a valid identifier.\n")
        return declaration

    def Assignment(self):
        assignment = False
        self.output.append("<Assignment> -> <Identifier> = <Expression>;\n")

        if self.token_is('='):
            if self.Expression():
                assignment = True
            else:
                self.output.append("Error: Invalid expression.\n")
        else:
            self.output.append("Error: Missing '='.\n")

        if not self.token_in(Constants.VALID_EOL_SYMBOLS):
            self.output.append("Warning: Missing ';' at end of line.\n")

        return assignment

    def If_Statement(self):
        ifstate = False
        self.output.append("<If-Statement> -> if <Conditional> then <Statement> <Else>\n")

        if self.Conditional():
            if self.token_is("then"):
                self.Statement()
                ifstate = self.Else()
            else:
                self.output.append("Error: Missing \"then\" keyword in If-Statement.\n")
        else:
            self.output.append("Error: Invalid conditional expression.\n")

        return ifstate

    def Conditional(self):
        conditional = False
        self.output.append("<Conditional> -> <Expression> <Conditional-Operator> <Expression>\n")

        if self.Expression():
            if self.token_in(Constants.VALID_CONDITIONAL_OPERATORS):
                if self.Expression():
                    conditional = True
            else:
                self.output.append("Error: Unrecognized conditional operator.\n")

        return conditional

    def Else(self):
        if self.token_is("else"):
            self.output.append("<Else> -> else <Statement>\n")
            self.Statement()
        else:
            self.output.append("<Else> -> epsilon\n")

        return True

    def For_Loop(self):
        for_loop = False
        self.output.append("<For-loop> -> for (<Declaration><conditional>;<Declaration>) {<Statement>};\n")
        if self.token_is("("):
            self.Declaration()
            self.Conditional()
            if self.token_is(";"):
                self.Declaration()
                if self.token_is(")"):
                    if self.token_is("{"):
                        self.Statement()
                        if self.token_is("}"):
                            if self.token_is(";"):
                                for_loop = True
        else:
            self.output.append("Error: For loop missing closing \"whileend\".\n")

        return for_loop

    def While_Loop(self):
        while_loop = False

        self.output.append("<While-Loop> -> while <Conditional> <Statement> whileend\n")
        if self.Conditional():
            self.Statement()

            if self.token_is("whileend"):
                while_loop = True
            else:
                self.output.append("Error: While loop missing closing \"whileend\".\n")

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

    def Factor(self):
        factor = True

        if self.is_current_token_an(LexerToken.IDENTIFIER):
            self.output.append("<Factor> -> <Identifier>\n")
            factor = True
        elif self.is_current_token_an(LexerToken.INTEGER):
            self.output.append("<Factor> -> <Integer>\n")
            factor = True
        elif self.is_current_token_an(LexerToken.REAL):
            self.output.append("<Factor> -> <Float>\n")
            factor = True
        elif self.is_current_token_an(LexerToken.BOOLEAN):
            self.output.append("<Factor> -> <Boolean>\n")
            factor = True
        elif self.token_is("("):
            self.output.append("<Factor> -> (<Expression>)\n")
            if (self.Expression()):
                if self.token_is(")"):
                    factor = True
                else:
                    self.output.append("Error: Missing closing ')' at end of expression.\n")
                    factor = False
            else:
                self.output.append("Error: Invalid expression.\n")
        else:
            self.output.append(
                "Error: Unrecognized value. Factor must be an integer, float, identifier or expression.\n")
            factor = False

        return factor
