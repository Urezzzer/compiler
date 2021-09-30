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

    def is_current_token_an(self, token_types):
        if self.tokens[self.current_token_index].token in token_types:
            self.advance_token()
            return True
        else:
            return False

    def backup(self, flag):
        if self.current_token_index > 0:
            self.current_token_index -= 1
            if flag == 'lexeme':
                value = self.tokens[self.current_token_index].lexeme
            if flag == 'token':
                value = self.tokens[self.current_token_index].token
            self.advance_token()
            return value

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def parse(self, tokens, positions, attributes, ids, errors):
        self.tokens = tokens
        self.positions = positions
        self.attributes = attributes
        self.ids = ids
        self.errors = errors

        while not self.is_current_token_an([LexerToken.END_OF_FILE]):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.ids.issuperset([self.backup('lexeme')]):
                    self.errors.append(Error(ErrorTypes.NOT_INITIALIZE, self.current_token_index))
                    self.output.append("Error: No inizializated identifier.\n")
            self.advance_token()
            if len(self.errors) != 0:
                break

    def write_output_to_file(self, filename):
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

        with open('C:\My Files\Python\Compilator\errors.txt', "w") as f:
            f.write("{:<20} {:<24}\n\n".format("ERROR", "INDEX_TOKEN"))
            for error in self.errors:
                f.write("{:<24} {:<24}\n".format(error.type, error.index))