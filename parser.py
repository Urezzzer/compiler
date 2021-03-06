from syntaxanalyser import SyntaxAnalyserRDP
from lexer import Lexer
from constants import *
from semanticanalyser import SemanticAnalyser
from codegenerator import CodeGenerator

import sys
import os


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.syntax_analyser = SyntaxAnalyserRDP()
        self.semantic_analyser = SemanticAnalyser()
        self.code_generator = CodeGenerator()

    def parse(self, input_file, output_file_for_lexer, output_file_for_syntax, output_file_for_semantic,
              output_file_for_generator):
        if os.path.exists(input_file):
            with open(input_file, "r") as f:
                for line in f:
                    if line != "\n":
                        self.lexer.parse(line)
                    else:
                        self.lexer.current_pos['row'] = self.lexer.current_pos['row'] + 1

                self.lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
                if len(self.lexer.positions) > 1:
                    self.lexer.positions.append({'row': self.lexer.positions[-1]['row'], 'pos': self.lexer.positions[-1]['pos'] + 1})
                self.syntax_analyser.parse(self.lexer.lexicon, self.lexer.positions, self.lexer.errors)
                self.lexer.write_to_file(output_file_for_lexer)
                self.syntax_analyser.write_output_to_file(output_file_for_syntax)
                self.semantic_analyser.parse(self.syntax_analyser.tokens, self.syntax_analyser.positions,
                                             self.syntax_analyser.errors)
                self.semantic_analyser.write_output_to_file(output_file_for_semantic)

                self.code_generator.parse(self.lexer.lexicon, self.syntax_analyser.errors)
                self.code_generator.write_output_to_file(output_file_for_generator)

        else:
            print(f"File \"{input_file}\" does not exist in the current directory.")


def main():
    p = Parser()
    p.parse('./input.cpp', './output_lexer.txt',
            './output_syntax.txt', './output_semantic.txt', './output_generator.txt')


if __name__ == "__main__":
    main()
