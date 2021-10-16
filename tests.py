import tests
import sys
from parser import Parser


output_lexer = './output_lexer.txt'
output_syntax = './output_syntax.txt'
output_semantic = './output_semantic.txt'


# Проверка работоспособности комментариев
# def test_lexer_1():
# ...

# ...
# def test_syntax_1():
# ...


# Корректный тест на кол-во параметров
def test_semantic_func_1():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error', output_semantic)
    print(name, not result)


# Передаем параметров в функцию больше, чем есть в сигнатуре
def test_semantic_func_2():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Wrong count of arguments. [6,21]', output_semantic)
    print(name, result)


# Передаем параметров в функцию меньше, чем есть в сигнатуре
def test_semantic_func_3():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Wrong count of arguments. [6,17]', output_semantic)
    print(name, result)


# Наличие точки входа main во входном файле
def test_semantic_main_1():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Expected main function.', output_semantic)
    print(name, result)


# Сложение числа и строки, присваиваем результат в переменную
def test_semantic_type_1():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: string type does not support operators +, -, /, * . [2,16]', output_semantic)
    print(name, result)


# Сложение числа и строки косвенно через функции, присваиваем результат в переменную
def test_semantic_type_2():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Type of data. [6,14]', output_semantic)
    print(name, result)


# Присваиваем число в строку косвенно через функцию
def test_semantic_type_3():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Type of data. [7,23]', output_semantic)
    print(name, result)


# Конкатенация строк
def test_semantic_type_4():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: string type does not support operators +, -, /, * . [2,27]', output_semantic)
    print(name, result)


# Сложение целых чисел (магические числа + целочисленный результат функции)
def test_semantic_type_5():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error', output_semantic)
    print(name, not result)


# Локальная переменная с одним названием в объявленной функции и точке входа
def test_semantic_visibility_1():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error', output_semantic)
    print(name, not result)


# Присваиваем значение переменной, которая пропала из области видимости
def test_semantic_visibility_2():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Not initialized a variable.  [6,5]', output_semantic)
    print(name, result)


# Проверяем, что переменную, объявленную в цикле, не видно снаружи
def test_semantic_visibility_3():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Not initialized a variable.  [6,5]', output_semantic)
    print(name, result)


# Проверяем, что переменная не объявлена
def test_semantic_visibility_4():
    name = sys._getframe().f_code.co_name
    parse(name, output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Not initialized a variable.  [2,5]', output_semantic)
    print(name, result)


def parse(input_file, output_file_for_lexer, output_file_for_syntax, output_file_for_semantic):
    p = Parser()
    p.parse('./tests/' + input_file + '.cpp', output_file_for_lexer, output_file_for_syntax, output_file_for_semantic)


def find_string_in_file(string, filename):
    with open(filename) as f:
        return string in f.read()


if __name__ == "__main__":
    for i in dir(tests):
        if i.startswith('test_'):
            eval(i + '()')
