from constants import *


class CodeGenerator:
    def __init__(self):
        self.tokens = []
        self.flag = False
        self.count_of_t = 1
        self.current_token_index = 0
        self.output = []
        self.errors = []

    def parse(self, tokens: list, errors: list):
        """Запуск программы"""
        self.tokens = tokens
        self.errors = errors
        if len(tokens) > 1:
            if len(self.errors) != 0:
                self.output.append("There is an error in the syntax of the code")
                return
            while not self.is_current_token_an([LexerToken.END_OF_FILE]):
                self.Start()
            self.output.append("\n\n\nif __name__ == " + '"__main__":\n    main()\n')
        else:
            self.output.append("Empty file.\n")

    def write_output_to_file(self, filename: str):
        """Записывает output в текстовый файл"""
        with open(filename, "w") as f:
            for line in self.output:
                f.write(line)

    def token_is(self, token_to_match: str) -> bool:
        """Проверяет текущий токен на равенство с переданным"""
        if self.tokens[self.current_token_index].lexeme == token_to_match:
            self.advance_token()
            return True
        else:
            return False

    def token_in(self, token_list: list) -> bool:
        """Проверяет текущий токен на вхождение в переданную группу"""
        if len(token_list) == 1:
            return self.token_is(token_list[0])
        else:
            if self.tokens[self.current_token_index].lexeme in token_list:
                self.advance_token()
                return True
            else:
                return False

    def is_current_token_an(self, token_types: list) -> bool:
        """Проверяет текущий токен на вхождение в переданный тип токенов"""
        if self.tokens[self.current_token_index].token in token_types:
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        """Метод для перехода к следующему токену"""
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def indentation(self):
        """Метод для расставления отступов"""
        if not self.output[-1] == "):\n":
            self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")

    def Start(self):
        """Старт"""
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.token_is('('):
                    if not self.output:
                        self.output.append("def " + self.tokens[self.current_token_index-2].lexeme + "(")
                    else:
                        self.output.append("\n\ndef " + self.tokens[self.current_token_index-2].lexeme + "(")
                    if self.Initialization():
                        self.token_is(')')
                        self.token_is('{')
                        while not self.token_is("}"):
                            self.Statement()

    def Statement(self) -> bool:
        """Проверка текущего оператора и запуск соответствующего состояния"""
        start = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.indentation()
            start = self.Assignment()
        elif self.token_in(Constants.VALID_DATA_TYPES):
            self.indentation()
            start = self.Declaration()
        elif self.token_is("if"):
            start = self.If_Statement()
            self.count_of_t -= 1
        elif self.token_is("for"):
            start = self.For_Loop()
            self.count_of_t -= 1
        elif self.token_is("while"):
            start = self.While_Loop()
            self.count_of_t -= 1
        elif self.token_is("return"):
            self.indentation()
            self.output.append("return ")
            start = self.Expression()
            self.token_in(Constants.VALID_EOL_SYMBOLS)

        return start


    def Declaration(self) -> bool:
        """Если текущий токен идентификатор, то запускается метод объявления переменной (запуск состояния объявления переменной.)"""
        declaration = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if self.Instruction():
                declaration = True

        return declaration

    def Assignment(self) -> bool:
        """Состояние вызова функции"""
        assignment = False
        if self.token_is('('):
            self.output.append(self.tokens[self.current_token_index-2].lexeme +
                               self.tokens[self.current_token_index-1].lexeme)
            if self.Function_Parameters():
                if self.token_is(')'):
                    self.output.append(")")
                self.token_in(Constants.VALID_EOL_SYMBOLS)
        elif self.Instruction():
            assignment = True

        return assignment

    def Initialization(self) -> bool:
        """Инициализация функций и её параметров"""
        initial = True
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                self.output.append(self.tokens[self.current_token_index-1].lexeme)
                if self.token_is(','):
                    self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
                    self.Initialization()
                else:
                    self.output.append("):\n")
            else:
                initial = False
        else:
            self.output.append("):\n")

        return initial

    def Instruction(self) -> bool:
        """Состояние объявления переменной"""
        instruction = False
        operator_token = self.tokens[self.current_token_index-1].lexeme
        if self.token_is('='):
            self.output.append(operator_token + " " + self.tokens[
                self.current_token_index - 1].lexeme + " ")
            if self.Expression():
                instruction = True
            if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                instruction = False

        return instruction

    def If_Statement(self) -> bool:
        """Состояние If"""
        ifstate = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.count_of_t += 1
        if self.token_is("("):
            if self.Conditional(False):
                if self.token_is(")"):
                    self.output[-1] = self.output[-1].strip()
                    self.output.append(":")
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            self.Statement()
                        ifstate = self.Else()
        self.flag = False
        return ifstate

    def Conditional(self, flag: bool) -> bool:
        """Состояние обработки условий"""
        conditional = False
        if flag:
            self.advance_token()
            self.advance_token()
            if self.token_is("="):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("!"):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("<") or self.token_is(">"):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme + "):")
                    self.advance_token()
                    conditional = True
                else:
                    self.output.append(self.tokens[self.current_token_index].lexeme + "):")
                    self.advance_token()
                    conditional = True
        else:
            if self.Expression():
                operator_token = self.tokens[self.current_token_index].lexeme
                if self.token_is("="):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("!"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("<") or self.token_is(">"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                    else:
                        self.output.append(" ")
                        if self.Expression():
                            conditional = True

        return conditional

    def Else(self) -> bool:
        """Состояние обработки ветки else"""
        if self.token_is("else"):
            self.output.append("\n")
            self.count_of_t -= 1
            for i in range(self.count_of_t):
                self.output.append("\t")
            self.count_of_t += 1
            self.output.append(self.tokens[self.current_token_index-1].lexeme + ":")
            if self.token_is("{"):
                while not self.token_is("}"):
                    self.Statement()
        return True

    def For_Loop(self) -> bool:
        """Состояние обработки цикла for"""
        for_loop = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.count_of_t += 1
        if self.token_is("("):
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.output.append(self.tokens[self.current_token_index].lexeme + " in range(")
                self.advance_token()
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme + ", ")
                    self.advance_token()
                if self.Conditional(True):
                    while not self.token_is("{"):
                        self.advance_token()
                    while not self.token_is("}"):
                        self.Statement()
        self.flag = False
        return for_loop

    def While_Loop(self) -> bool:
        """Состояние обработки цикла while"""
        while_loop = False
        self.flag = True
        self.output.append("\n")
        for i in range(self.count_of_t):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index-1].lexeme + " ")
        self.count_of_t += 1
        if self.token_is("("):
            self.Conditional(False)
            if self.token_is(")"):
                self.output[-1] = self.output[-1].strip()
                self.output.append(":")
                if self.token_is("{"):
                    while not self.token_is("}"):
                        self.Statement()
        self.flag = False
        return while_loop

    def Expression(self) -> bool:
        """Состояние обработки выражений"""
        expression = False
        if self.Term():
            if self.Expression_Prime():
                expression = True

        return expression

    def Expression_Prime(self) -> bool:
        """Обработка сложения и вычитания"""
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append(" " + operator_token + " ")
            if not self.Term():
                expression_prime = False
            else:
                if not self.Expression_Prime():
                    expression_prime = False

        return expression_prime

    def Term(self) -> bool:
        """ """
        term = False
        if self.Factor():
            if self.Term_Prime():
                term = True

        return term

    def Term_Prime(self) -> bool:
        """Обработка произведения и деления"""
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append(" " + operator_token + " ")
            if not self.Factor():
                term_prime = False
            else:
                if not self.Term_Prime():
                    term_prime = False

        return term_prime

    def Function_Parameters(self) -> bool:
        """Обработка аргументов функций"""
        function_parameters = True
        if self.Expression():
            if self.token_is(","):
                self.output.append(", ")
                self.Function_Parameters()

        return function_parameters

    def Factor(self) -> bool:
        """Обработка значений переменной"""
        factor = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_in(Constants.SIGNED_OPERATORS):
            self.output.append(operator_token)
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False
        else:
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.BOOLEAN]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.token_is('"') or self.token_is("'"):
                self.output.append(self.tokens[self.current_token_index-1].lexeme +
                                   self.tokens[self.current_token_index].lexeme)
                self.is_current_token_an([LexerToken.STRING])
                if not (self.token_is('"') or self.token_is("'")):
                    factor = False
                else:
                    self.output.append(self.tokens[self.current_token_index-1].lexeme)
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False

        return factor
