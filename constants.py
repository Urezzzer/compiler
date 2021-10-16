from enum import Enum
from collections import namedtuple

Listing = namedtuple("Listing", "lexeme, token")
Error = namedtuple("Error", ['type', 'index'])


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
    NOT_EXISTS = 11,
    COMMENT = 12


# states
class LexerState(Enum):
    START = 0,
    INTEGER = 1,
    REAL = 2,
    ALPHABETIC = 3,
    OPERATOR = 4,
    COMMENT = 5,
    INVALID = 6,
    STRING = 7,
    SLASH = 8


class ErrorTypes(Enum):
    INVALID = 0,
    MISSING = 1,
    INITIALIZATION = 2,
    WRONG_TYPE = 3,
    MISSING_MAIN = 4,
    EXPECTED = 5


class Constants(object):
    VALID_OPERATORS = ["+", "-", "=", "*", "<", ">", "!"]
    SIGNED_OPERATORS = ["+", "-"]
    VALID_SEPARATORS = ["(", ")", "[", "]", "{", "}", ",", ";", ".", ":"]
    VALID_STRING = ['"', "'"]
    VALID_KEYWORDS = ["int", "float", "bool", "if", "else", "then", "while", "double", "std::string",
                      "string", "void", "return", "for"]

    DECIMAL = '.'
    SLASH = "/"
    VALID_IDENTIFIER_SYMBOLS = "$"
    VALID_EOL_SYMBOLS = [';']
    TOKEN_END_OF_LINE = Listing("$", LexerToken.END_OF_FILE)
    VALID_DATA_TYPES = ["int", "bool", "float", "std::string", "double", "void"]
    VALID_BOOLEAN_VALUES = ["true", "false"]
