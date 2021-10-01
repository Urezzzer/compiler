import os

from constants import *


class Lexer(object):
    def __init__(self):
        self.buffer = []
        self.current_state = LexerState.START
        self.lexicon = []
        self.errors = []

        self.positions = []
        self.current_pos = {
            'row': 0,
            'pos': 0
        }

    def parse(self, line):
        self.current_pos['pos'] = 0
        for char in line:
            if char != Constants.SLASH and self.current_state == LexerState.SLASH:
                self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                self.add_to_lexicon('/', LexerToken.OPERATOR)
                self.return_to_start()
            if char.isalpha():
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.START:
                    self.current_state = LexerState.ALPHABETIC
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.INTEGER, LexerState.REAL]:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.return_to_start()
                elif self.current_state == LexerState.ALPHABETIC:
                    self.append_to_buffer(char)
            elif char.isnumeric():
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.START:
                    self.current_state = LexerState.INTEGER
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.INTEGER, LexerState.REAL, LexerState.ALPHABETIC]:
                    self.append_to_buffer(char)
            elif char == Constants.DECIMAL:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.INTEGER:
                    self.current_state = LexerState.REAL
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.ALPHABETIC, LexerState.REAL]:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.return_to_start()
            elif char in Constants.VALID_IDENTIFIER_SYMBOLS:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.ALPHABETIC:
                    self.append_to_buffer(char)
                else:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.return_to_start()
            elif char in Constants.VALID_SEPARATORS:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state != LexerState.COMMENT:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.SEPARATOR)
                    self.return_to_start()
            elif char in Constants.VALID_OPERATORS:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state != LexerState.COMMENT:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.return_to_start()
            elif char == Constants.SLASH:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                if self.current_state != LexerState.SLASH and self.current_state != LexerState.COMMENT:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.current_state = LexerState.SLASH
                else:
                    self.current_state = LexerState.COMMENT
            elif char in Constants.VALID_STRING:
                if self.current_state == LexerState.COMMENT:
                    self.append_to_buffer(char)
                if self.current_state != LexerState.STRING:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.current_state = LexerState.STRING
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.current_state = LexerState.START
            elif char == " ":
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.return_to_start()
            elif char == '\n':
                self.current_pos['row'] = self.current_pos['row'] + 1
                self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                self.current_state = LexerState.START
                self.buffer.clear()
            else:
                if self.current_state != LexerState.STRING:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.NOT_EXISTS)
                    self.errors.append(Error(ErrorTypes.NOT_VALID, LexerToken.NOT_EXISTS))
                    self.return_to_start()
                else:
                    self.append_to_buffer(char)
            self.current_pos['pos'] = self.current_pos['pos'] + 1

    def return_to_start(self):
        if self.current_state != LexerState.COMMENT:
            self.current_state = LexerState.START
            self.buffer.clear()

    def is_keyword(self, lexeme):
        if lexeme in Constants.VALID_KEYWORDS:
            return True
        else:
            return False

    def is_boolean(self, lexeme):
        if lexeme in Constants.VALID_BOOLEAN_VALUES:
            return True
        else:
            return False

    def append_to_buffer(self, char):
        if self.current_state != LexerState.COMMENT:
            self.buffer.append(char)

    def analyse_nonsymbol_lexeme(self, lexeme):
        if self.current_state == LexerState.STRING:
            self.add_to_lexicon(lexeme, LexerToken.STRING)
        elif self.current_state == LexerState.INTEGER:
            self.add_to_lexicon(lexeme, LexerToken.INTEGER)
        elif self.current_state == LexerState.REAL:
            self.add_to_lexicon(lexeme, LexerToken.REAL)
        elif self.current_state == LexerState.ALPHABETIC:
            if self.is_keyword(lexeme):
                self.add_to_lexicon(lexeme, LexerToken.KEYWORD)
            elif self.is_boolean(lexeme):
                self.add_to_lexicon(lexeme, LexerToken.BOOLEAN)
            else:
                self.add_to_lexicon(lexeme, LexerToken.IDENTIFIER)

    def add_to_lexicon(self, token, lexeme):
        new_listing = Listing(token, lexeme)
        self.positions.append(self.current_pos.copy())
        self.lexicon.append(new_listing)

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write("{:<12} {:<24}\n\n".format("TOKENS", "LEXEMES"))

            for entry in self.lexicon:
                f.write("{:<12} {:<24}\n".format(entry.token.name, entry.lexeme))

    def parse_file(self, input, output):
        if os.path.exists(input):
            with open(input, "r") as f:
                for line in f:
                    if line != "\n":
                        self.parse(line)
        self.write_to_file(output)