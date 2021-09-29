from parser import *
from lexer import *

import sys


# def main():
#    p = Parser()
#    p.parse(sys.argv[1], sys.argv[2])

def main():
    l = Lexer()
    l.parse_file('C:\My Files\Python\Compilator\input.txt', 'C:\My Files\Python\Compilator\output.txt')


if __name__ == "__main__":
    main()
