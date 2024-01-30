#!/usr/bin/env python3

# USAGE:
# python3 compiler.py [input_file [output_file]]


"""
Aluno: Mateus Dias Louzada

Colegas participantes: Paulo Neto, Leonardo Heldt, Bernardo Castello
"""
import sys
from sly import Lexer, Parser

#################### LEXER ####################

var_table = []

class ÇLexer(Lexer):
    
    # token definitions
    literals = {';', '+', '-', '*', '/', '(', ')', '{', '}', '[', ']', ',', '=', '%'}
    tokens = {STDIO,VOID, INT, MAIN, PRINTF, STRING, NUMBER, NAME, IF, WHILE, COMPARATOR}
    STDIO   = '#include <stdio.h>'
    VOID    = 'void'
    INT     = 'int'
    MAIN    = 'main'
    PRINTF  = 'printf'
    IF      = 'if'
    WHILE   = 'while'
    STRING  = r'"[^"]*"'
    NUMBER  = r'\d+'
    NAME    = r'[a-z]+'
    
    COMPARATOR = r'(==|>=|<=|!=|>|<)'

    # ignored characters and patterns
    ignore = r' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'//[^\n]*'

    # extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # error handling method
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' in line {self.lineno}")
        self.index += 1

#################### PARSER ####################

class ÇParser(Parser):
    tokens = ÇLexer.tokens

    def __init__(self):
        self.symbol_table = []
        self.if_counter = 1
        self.if_stack = []
        self.while_stack = []
        self.while_counter = 0
        self.symbol_array = []

    # error handling method
    def error(self, mesg):
        print(mesg, file=sys.stderr)
        sys.exit(1)
        
    # ---------------- program ----------------
    
    @_('stdio functions main')
    def program(self, p):
        print('\n# symbol_table:', var_table)
        print('\n# symbol_array:', self.symbol_array)
    
    @_('STDIO')
    def stdio(self, p):
        print('LOAD_CONST 0')
        print('LOAD_CONST None')
        print('IMPORT_NAME runtime')
        print('IMPORT_STAR')
    
    # ----------------functions ---------------
    @_('function functions')
    def functions(self, p):
        pass
    
    @_('')
    def functions(self, p):
        pass
    

    @_('NAME "(" parameters ")"')
    def function_name(self, p):
        print('.begin', p.NAME, p.parameters)
        for name in p.parameters:
            var_table.append(name)

    @_('VOID function_name  "{" statements "}"')
    def function(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')
        print('.end')
        print('# symbol_table', var_table)
        var_table.clear()       
    #---------------- parameters -----------
    
    @_('INT NAME "," parameters')
    def parameters(self, p):
        return p.NAME + ' ' + p.parameters
    
    @_('INT NAME')
    def parameters(self, p):
        return p.NAME

    @_('')
    def parameters(self, p):
        return ''
    

    # ---------------- main ----------------

    @_('INT MAIN "(" ")" "{" statements "}"')
    def main(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')

    # ---------------- statements ----------------

    @_('statement statements')
    def statements(self, p):
        pass

    @_('')
    def statements(self, p):
        pass

    # ---------------- statement ----------------

    @_('printf')
    def statement(self, p):
        print()

    @_('declaration')
    def statement(self, p):
        print()

    @_('attribution')
    def statement(self, p):
        print()
    
    @_('if_st')
    def statement(self, p):
        print()
    
    @_('while_st')
    def statement(self, p):
        print()
    
    @_('decl_array')
    def statement(self, p):
        print()

    @_('attr_array')
    def statement(self, p):
        print()
        
    @_('decl_array2')
    def statement(self, p):
        print()

    @_('call')
    def statement(self, p):
        print()
    

    # ---------------- call ----------------
    @_('NAME')
    def call_name(self, p):
        print('LOAD_NAME', p.NAME)
    
    @_('call_name "(" arguments ")" ";"')
    def call(self, p):
        print('CALL_FUNCTION', p.arguments)
        print('POP_TOP')


    # ----------------- arguments -----------
    @_('expression "," arguments')
    def arguments(self, p):
        return 1 + p.arguments
    
    @_('expression')
    def arguments(self, p):
        return 1

    @_('')
    def arguments(self, p):
        return 0



    # ---------------- printf ----------------

    @_('STRING')
    def printf_format(self, p):
        print('LOAD_GLOBAL', 'print')
        print('LOAD_CONST', p.STRING)

    @_('PRINTF "(" printf_format "," expression ")" ";"')
    def printf(self, p):
        
        print('BINARY_MODULO')
        print('CALL_FUNCTION', 1)
        print('POP_TOP')

    # ---------------- declaration ----------------
    
    @_('INT NAME "=" expression ";"')
    def declaration(self, p):
        if p.NAME in var_table:
            self.error(f'Error: Variable "{p.NAME}" has already been declared previously.')
        else:
            var_table.append(p.NAME)
            print('STORE_FAST', p.NAME)

    # ---------------- attribution ----------------

    @_('NAME "=" expression ";"')
    def attribution(self, p): 
        
        if p.NAME not in var_table:
            self.error(f'Error: Variable "{p.NAME}" not declared.')
            sys.exit(1)
        else:
            print('STORE_FAST', p.NAME)

    # ---------------- decl_array ----------------

    @_('INT NAME "[" "]" "=" "{" expressions "}" ";"')
    def decl_array(self, p):
        print('BUILD_LIST ' + str(p.expressions))
       
        if p.NAME in self.symbol_array:
            self.error(f'Error: Variable "{p.NAME}" has already been declared previously.')
        else:
            self.symbol_array.append(p.NAME)
            print('STORE_NAME', p.NAME)

    @_('expression "," expressions')
    def expressions(self, p):
        return 1 + p.expressions

    @_('expression')
    def expressions(self, p):
        #gera codigo e deixa na pilha
        return 1
    
    
    
    # ----------- decl_array 2 ---------------- 


    @_('')
    def array_size(self, p):
        print('LOAD_NAME array_zero') 

    @_('INT NAME  "[" array_size expressions "]" ";"')
    def decl_array2(self, p):
        print('CALL_FUNCTION 1')
        print('STORE_NAME ' + p.NAME)
        self.symbol_array.append(p.NAME)
    
    # ---------------- attr_array ----------------

    @_('name_array "[" expression "]" "=" expression ";"')
    def attr_array(self, p):
        print('ROT_THREE')
        print('STORE_SUBSCR')
    
    @_('NAME')
    def name_array(self, p):
        if p.NAME not in self.symbol_array:
            self.error(f'Error: Unkown variable "{p.NAME}"')
            sys.exit(1)
        else:
            print('LOAD_NAME', p.NAME)

    # ---------------- if ----------------

    @_('expression COMPARATOR expression')
    def if_comparison(self, p):
        
        print('COMPARE_OP', p.COMPARATOR)
        print('POP_JUMP_IF_FALSE', f'NOT_IF_{self.if_counter}')
        self.if_stack.append(f'NOT_IF_{self.if_counter}')
        self.if_counter += 1

    @_('IF "(" if_comparison ")" "{" statements "}"')
    def if_st(self, p):

        print(self.if_stack.pop() + ':')

    # ---------------- while ----------------

    @_('WHILE')
    def while_begin(self, p):

        self.while_counter += 1
        print(f'BEGIN_WHILE_{self.while_counter}:')
        
    @_('expression COMPARATOR expression')
    def while_comparison(self, p):
        
        print('COMPARE_OP', p.COMPARATOR)
        print('POP_JUMP_IF_FALSE', f'END_WHILE_{self.while_counter}')
        self.while_stack.append(self.while_counter)

    @_('while_begin "(" while_comparison ")" "{" statements "}"')
    def while_st(self, p):
        
        ID = self.while_stack.pop()
        print('JUMP_ABSOLUTE', f'BEGIN_WHILE_{ID}')
        print(f'END_WHILE_{ID}:')

    # ---------------- expression ----------------

    @_('expression "+" term')
    def expression(self, p):
        print('BINARY_ADD')

    @_('expression "-" term')
    def expression(self, p):
        print('BINARY_SUBTRACT')

    @_('term')
    def expression(self, p):
        pass

    # ---------------- term ----------------

    @_('term "*" factor')
    def term(self, p):
        print('BINARY_MULTIPLY')

    @_('term "/" factor')
    def term(self, p):
        print('BINARY_FLOOR_DIVIDE')

    @_('term "%" factor')
    def term(self, p):
        print('BINARY_MODULO')

    @_('factor')
    def term(self, p):
        pass

    # ---------------- factor ----------------
    
    @_('NUMBER')
    def factor(self, p):
        
        print('LOAD_CONST', p.NUMBER)

    @_('"(" expression ")"')
    def factor(self, p):
        pass

    @_('name_array "[" expression "]"')
    def factor(self, p):
        
        print('BINARY_SUBSCR')
    
    @_('NAME')
    def factor(self, p):
        
        if p.NAME not in var_table and p.NAME not in self.symbol_array:
            self.error(f'Error: Unkown variable "{p.NAME}"')
            sys.exit(1)
        else:
            print('LOAD_FAST', p.NAME)

#################### MAIN ####################

lexer = ÇLexer()
parser = ÇParser()

if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')
    
    if len(sys.argv) > 2:
        sys.stdout = open(sys.argv[2], 'w')

text = sys.stdin.read()
parser.parse(lexer.tokenize(text))
