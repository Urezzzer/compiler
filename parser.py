from syntaxanalyser import SyntaxAnalyserRDP
from lexer import Lexer
from constants import *

import os


class Parser:
    def __init__(self):
        self.tokens = []
        self.lexer = Lexer()
        self.syntax_analyser = SyntaxAnalyserRDP()

    def parse(self, input_file, output_file):
        if os.path.exists(input_file):
            with open(input_file, "r") as f:
                for line in f:
                    if line != "\n":
                        self.lexer.parse(line)

                self.lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
                self.syntax_analyser.parse(self.lexer.lexicon)
                self.syntax_analyser.write_output_to_file(output_file)
        else:
            print(f"File \"{input_file}\" does not exist in the current directory.")
