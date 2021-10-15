from parser import Parser


output_lexer = './tests/output_lexer.txt'
output_syntax = './tests/output_syntax.txt'
output_semantic = './tests/output_semantic.txt'

# Проверка работоспособности комментариев
# def test_lexer_1():
# ...

# ...
# def test_syntax_1():
# ...

# Наличие точки входа main во входном файле
def test_semantic_1():
    parse('./tests/test_semantic_1.cpp', output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Expected main function.', output_semantic)
    print('test_semantic_1', result)


# Сложение числа и строки, запись результата в переменную
def test_semantic_2():
    parse('./tests/test_semantic_2.cpp', output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: string type does not support operators +, -, /, * . [2,16]', output_semantic)
    print('test_semantic_2', result)


# Сложение числа и строки косвенно через функции, запись результата в переменную
def test_semantic_3():
    parse('./tests/test_semantic_3.cpp', output_lexer, output_syntax, output_semantic)
    result = find_string_in_file('Error: Type of data. [6,14]', output_semantic)
    print('test_semantic_3', result)


def parse(input_file, output_file_for_lexer, output_file_for_syntax, output_file_for_semantic):
    p = Parser()
    p.parse(input_file, output_file_for_lexer, output_file_for_syntax, output_file_for_semantic)


def find_string_in_file(string, filename):
    with open(filename) as f:
        return string in f.read()


if __name__ == "__main__":
    test_semantic_1()
    test_semantic_2()
    test_semantic_3()
