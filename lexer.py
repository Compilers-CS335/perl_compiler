#!/usr/bin/python
import lex


#reserved words
reserved={
	'if' : 'IF',
	'else':'ELSE',
	'elsif':'ELSIF',
	'unless':'UNLESS',
	'switch':'SWITCH',
	'case':'CASE',
	'while':'WHILE',
	'until':'UNTIL',
	'for':'FOR',
	'foreach':'FOREACH',
	'do':'DO',
	'next':'NEXT',
	'last':'LAST',
	'continue':'CONTINUE',
	'redo':'REDO',
	'goto':'GOTO',
	'and':'AND_OP',
	'or':'OR_OP',
	'not':'NOT_OP',
	'use':'USE',
	'sub':'SUB',
	'my':'PRIVATE',
	'local':'LOCAL',
	'format':'FORMAT',
	'write':'WRITE',
	'select':'SELECT'
}
# I am bored avikalp please complete the list
# completed the list from the list of reserved words as in the file reserved.txt
# I have given 'and', 'or' and 'not' the same name as the tokens below
# 'my' ko especially PRIVATE  naam diya hai... dont ask why :P

#some tokens we are gonna use 
tokens=[
		"STRING",
		"RES_STRING",
		"NUMBER",
		"PLUS_OP",
		"MINUS_OP",
		"MULTIPLICATION_OP",
		"DIVISION_OP",
		"MODULUS_OP",
		"EXPONENT_OP",
		"FLOOR_DIVISION_OP",
		"NOT_OP",
		"AND_OP",
		"OR_OP",
		"COMPARE_OP",
		"NOT_EQUALS_OP",
		"EQUALS_OP",
		"GREATER_EQUAL_OP",
		"GREATER_OP"
		"LESS_EQUAL_OP",
		"LESS_OP",
		"ASSIGNMENT_OP",
		"SEMICOLON",
		"BLOCK_BEGIN",
		"BLOCK_ENDS",
		"OPEN_BRACKET",
		"CLOSE_BRACKET",
		"OPEN_PARANTHESIS",
		"CLOSE_PARANTHESIS",
		"COMMA",
		"IDENTIFIER",
		"WHITESPACE",
		"COMMENT"
		] + list(reserved.values())

t_ignore_WHITESPACE=r"\s"




def t_STRING(t):
	r"\'(\\.|[^\'])*\'"
	return t

def t_RES_STRING(t):
	r"\"(\\.|[^\"])*\""
	return t
	
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_EXPONENT_OP(t):
	r"\*\*"
	return t

def t_PLUS_OP(t):
	r"\+"
	return t

def t_MINUS_OP(t):
	r"-"
	return t

def t_MULTIPLICATION_OP(t):
	r"\*"
	return t

def t_DIVISION_OP(t):
	r"/"
	return t

def t_MODULUS_OP(t):
	r"%"
	return t

def t_SEMICOLON(t):
	r";"
	return t

def t_BLOCK_BEGIN(t):
	r"\{"
	return t

def t_BLOCK_ENDS(t):
	r"\}"
	return t

def t_OPEN_BRACKET(t):
	r"\["
	return t

def t_CLOSE_BRACKET(t):
	r"\]"
	return t

def t_OPEN_PARANTHESIS(t):
	r"\("
	return t

def t_CLOSE_PARANTHESIS(t):
	r"\)"
	return t

def t_COMMA(t):
	r","
	return t

def t_EQUALS_OP(t):
	r"=="
	return t

def t_NOT_EQUALS_OP(t):
	r"\!="
	return t

def t_NOT_OP(t):
	r"\!"
	return t

def t_COMPARE_OP(t):
	r"<=>"
	return t

def t_GREATER_EQUAL_OP(t):
	r">="
	return t

def t_LESS_EQUAL_OP(t):				#I have no clue why is this not working
	r"<="
	return t

def t_GREATER_OP(t):				# No clue  why this is not working
	r">"
	return t

def t_LESS_OP(t):
	r"<"
	return t

def t_AND_OP(t):
	r"&&"
	return t

def t_OR_OP(t):
	r"\|\|"
	return t

def t_ASSIGNMENT_OP(t):
	r"=|"r"\+=|"r"-=|"r"\*=|"r"/=|"r"%="
	return t

def t_ignore_COMMENT(t):
	r"\#.*"
	
#newline
def t_newline(t):
	r"(\n)+"
	t.lexer.lineno+=len(t.value)

#error	
def t_error(t):
	print "Illegal character %s" % t.value[0]
	t.lexer.skip(1)

#identifier
def t_IDENTIFIER(t):
    r"[\$@%]?[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    
    return t

lexer=lex.lex()
def runlexer(inputfile):
	program=open(inputfile).read()
	lexer.input(program)
	print "Type \t\t\t\t\t Value"
	for tok in iter(lexer.token, None):
		print "%s \t\t\t\t\t %s" %(repr(tok.type),repr(tok.value))
	

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runlexer(inputfile)
