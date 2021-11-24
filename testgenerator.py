import sys
import os
from parser import Parser

output_lexer = './output_lexer.txt'
output_syntax = './output_syntax.txt'
output_semantic = './output_semantic.txt'
path_generator = './generator_tests_results/'


# Тест на код с ошибкой
def test_generator_code_with_error():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


# Передаем параметров в функцию больше, чем есть в сигнатуре
def test_generator_for():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


# Передаем параметров в функцию меньше, чем есть в сигнатуре
def test_generator_functions():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


# Наличие точки входа main во входном файле
def test_generator_if_else():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


# Сложение числа и строки, присваиваем результат в переменную
def test_generator_programm():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


# Сложение числа и строки косвенно через функции, присваиваем результат в переменную
def test_generator_while():
    name = sys._getframe().f_code.co_name
    output_generator = path_generator + name + ".py"
    parse(name, output_lexer, output_syntax, output_semantic, output_generator)


def parse(input_file, output_file_for_lexer, output_file_for_syntax, output_file_for_semantic,
          output_file_for_generator):
    p = Parser()
    p.parse('./tests_generator/' + input_file + '.cpp', output_file_for_lexer, output_file_for_syntax,
            output_file_for_semantic, output_file_for_generator)


def find_string_in_file(string, filename):
    with open(filename) as f:
        return string in f.read()


if __name__ == "__main__":
    if not os.path.isdir('./generator_tests_results'):
        os.mkdir('./generator_tests_results')
    for i in dir():
        if i.startswith('test_'):
            eval(i + '()')