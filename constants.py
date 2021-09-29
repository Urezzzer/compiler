from enum import Enum
from collections import namedtuple

Listing = namedtuple("Listing", "lexeme, token")


# token types
class LexerToken(Enum):
    KEYWORD = 1,
    OPERATOR = 2,
    SEPARATOR = 3,
    INTEGER = 4,
    REAL = 5,
    IDENTIFIER = 6,
    INVALID = 7,
    END_OF_FILE = 8,
    BOOLEAN = 9,
    STRING = 10,
    NOT_EXISTS = 11


# states
class LexerState(Enum):
    START = 0,
    INTEGER = 1,
    REAL = 2,
    ALPHABETIC = 3,
    OPERATOR = 4,
    COMMENT = 5,
    INVALID = 6


class Constants(object):
    VALID_OPERATORS = ["+", "-", "=", "*", "/", "%"]
    VALID_SEPARATORS = ["(", ")", "[", "]", "{", "}", ",", ";", ".", ":"]
    VALID_STRING = ['"', "'" ]
    VALID_KEYWORDS = ["int", "float", "bool", "if", "else", "then", "while", "const", "main", "char", "double",
                      "string", "void", "return", "do", "for", "auto", ]

    DECIMAL = '.'
    COMMENT_START = ["/*", "//"]
    COMMENT_END = "*/"
    VALID_IDENTIFIER_SYMBOLS = ["$"]
    VALID_EOL_SYMBOLS = [';']
    TOKEN_END_OF_LINE = Listing("$", LexerToken.END_OF_FILE)
    VALID_CONDITIONAL_OPERATORS = ["=", "<", ">", "!"]
    VALID_DATA_TYPES = ["int", "bool", "float", "char", "string", "double", "void", "auto"]
    VALID_BOOLEAN_VALUES = ["true", "false"]
