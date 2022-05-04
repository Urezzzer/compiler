# Description
* lexer.py - implementation of a lexical analyzer
* syntaxanalyzer.py - implementation of a syntax analyzer
* semanticanalyser.py - implementation of a semantic analyzer

* constants.py - constants, states and types of tokens
* grammar.py - used grammar

### parser.py - объединение 3 анализаторов - a parser that parses C++ code to Python code using abpve blocks

* Input: input.cpp - C++ code
* Output: errors.txt - error logs, output_lexer.txt - lexer traverse, output_semantic.txt - semantic traverse, output_syntax.txt - syntax traverse
#### It misdetermines position of error if code has no space symbols between operators. May be fixed :)
