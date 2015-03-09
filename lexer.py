#!/usr/bin/python
import lex
#from ply import lex

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
	'use':'USE',
	'sub':'SUB',
	'my':'PRIVATE',
	'local':'LOCAL',
	'format':'FORMAT',
	'print' : 'PRINT',
	'return':'RETURN',
	'write':'WRITE',
	'select':'SELECT'
}
# completed the list from the list of reserved words as in the file reserved.txt
# I have given 'and', 'or' and 'not' the same name as the tokens below
# 'my' ko especially PRIVATE  naam diya hai... dont ask why :P

#some tokens we are gonna use 
tokens=[
		"STRING",
		"RES_STRING",			#responsive strings
		"SCI_NOT",				#numbers in scientific notation
		"NUMBER",				#positive or negative integers
		"FLOAT",
		"OCTAL",
		"HEXADECIMAL",
		"PLUS_OP",
		"MINUS_OP",
		"MULTIPLICATION_OP",
		"DIVISION_OP",
		"MODULUS_OP",
		"EXPONENT_OP",
		"REP_OP",				#the repetition operator 'x'
		"NOT_OP",
		"AND_OP",
		"OR_OP",
		"NOT_STR_OP",
		"AND_STR_OP",
		"OR_STR_OP",
		"XOR_STR_OP",
		"COMPARE_OP",
		"NOT_EQUALS_OP",
		"EQUALS_OP",
		"GREATER_EQUAL_OP",
		"GREATER_OP",
		"LESS_EQUAL_OP",
		"LESS_OP",
		"ADV_ASSIGNMENT_OP",	#those which do an operation before assignment
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
		"COMMENT",
		"BIT_AND",
		"BIT_OR",
		"BIT_XOR",
		"BIT_FLIP",
		"BIT_LEFT_SHIFT",
		"BIT_RIGHT_SHIFT",
		"CONCATENATE",
		"SEARCH_MODIFY",		#the operator used to search in and/or modify strings
		"SEARCH_MODIFY_NEG",	#same as above but returns the negation
		"RANGE_OP",				#the one used in 2..6
		"USER_INPUT_OP",
		"MATCH",				# http://affy.blogspot.in/p5be/ch10.htm
		"SUBSTITUTE",
		"TRANSLATION",
		"SYSTEM_COMMAND",
		"VARIABLE",
		"ARRAY",
		"HASH",
		"QUESTION_MARK",
		"COLON",
		"INCREMENT_OP",
		"DECREMENT_OP",
		"FILE_HANDLING_OPTIONS",
		"ASSOCIATE_OP"
		] + list(reserved.values())

t_ignore_WHITESPACE=r"\s"




def t_STRING(t):
	r"\'([^\'])*\'"
	return t

def t_RES_STRING(t):
	r"\"(\\.|[^\"])*\""
	return t

def t_USER_INPUT_OP(t):
	r"<([A-Z\*]+)?>"
	return t

def t_SCI_NOT(t):
    r"(\d+\.\d+|\d+)[eE](-)?\d+"
    # t.value = float(t.value)
    return t
	
def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t

def t_HEXADECIMAL(t):
    r"[0][x][a-fA-F0-9]+"
    # t.value = int(t.value, 16)
    return t
	
def t_OCTAL(t):
    r"[0][0-7]+"
    # t.value = int(t.value)
    return t	

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_ADV_ASSIGNMENT_OP(t):
	r"\+=|"r"-=|"r"\*=|"r"/=|"r"%=|"r"\*\*=|"r"\.=|"r"x="
	return t

def t_ASSOCIATE_OP(t):
	r"=>"
	return t

def t_EXPONENT_OP(t):
	r"\*\*"
	return t

def t_MATCH(t):							# This definition is not complete as match can also be used without 'm'
	r"m([ \t]*)?/(\\.|[^/])*/([gimosx])?"
	return t

def t_SUBSTITUTE(t):
	r"s([ \t]*)?/(\\.|[^/])*/(\\.|[^/])*/([egimosx])?"
	return t

def t_TRANSLATION(t):
	r"(tr|y)([ \t]*)?/(\\.|[^/])*/(\\.|[^/])*/([cds])?"
	return t

def t_INCREMENT_OP(t):
	r"\+\+"
	return t

def t_DECREMENT_OP(t):
	r"--"
	return t

def t_PLUS_OP(t):
	r"\+"
	return t

def t_FILE_HANDLING_OPTIONS(t):
	r"-[ABCMORSTWXbcdefghklmnoprstuwxz]"
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

def t_BIT_LEFT_SHIFT(t):
	r"<<"
	return t

def t_BIT_RIGHT_SHIFT(t):
	r">>"
	return t

def t_EQUALS_OP(t):
	r"==|"r"eq"
	return t

def t_NOT_EQUALS_OP(t):
	r"\!="
	return t

def t_COMPARE_OP(t):
	r"<=>|"r"cmp"
	return t

def t_GREATER_EQUAL_OP(t):
	r">=|"r"ge"
	return t

def t_LESS_EQUAL_OP(t):				
	r"<=|"r"le"
	return t

def t_GREATER_OP(t):				
	r">|"r"gt"
	return t

def t_LESS_OP(t):
	r"<|"r"lt"
	return t

def t_XOR_STR_OP(t):
	r"xor"
	return t

def t_AND_OP(t):
	r"&&"
	return t

def t_AND_STR_OP(t):
	r"and"
	return t

def t_OR_OP(t):
	r"\|\|"
	return t

def t_OR_STR_OP(t):
	r"or"
	return t

def t_SEARCH_MODIFY(t):
	r"=~"
	return t

def t_SEARCH_MODIFY_NEG(t):
	r"\!~"
	return t

def t_NOT_OP(t):
	r"\!"
	return t

def t_NOT_STR_OP(t):
	r"not"
	return t

#identifier
# def t_IDENTIFIER(t):
#     r"[\$@%]?[a-zA-Z$_][\w$]*"
#     t.type = reserved.get(t.value,'IDENTIFIER')    
#     return t

def t_VARIABLE(t):
    r"[\$][a-zA-Z$_][\w$]*"							# not considering $#
    t.type = reserved.get(t.value,'VARIABLE')    
    return t

def t_HASH(t):
    r"[%][a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'HASH')    
    return t

def t_ARRAY(t):
    r"[@][a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'ARRAY')    
    return t

def t_IDENTIFIER(t):
    r"[&]?[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    
    return t

def t_MODULUS_OP(t):
	r"%"
	return t

def t_REP_OP(t):
	r"x"
	return t

def t_BIT_AND(t):
	r"&"
	return t

def t_BIT_OR(t):
	r"\|"
	return t

def t_BIT_XOR(t):
	r"\^"
	return t

def t_BIT_FLIP(t):
	r"~"
	return t

def t_RANGE_OP(t):
	r"\.\."
	return t

def t_CONCATENATE(t):
	r"\."
	return t

def t_SYSTEM_COMMAND(t):
	r"\`([^\`])*\`"
	return t

def t_ASSIGNMENT_OP(t):
	r"="
	return t

def t_QUESTION_MARK(t):
	r"\?"
	return t

def t_COLON(t):
	r"\:"
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

lexer=lex.lex()
def runlexer(inputfile):
	program=open(inputfile).read()
	lexer.input(program)
	line1 = ""
	line2 = "#"
	LineNum = 0;
	for tok in iter(lexer.token, None):
		while tok.lineno!=LineNum:
		 	LineNum+=1
		 	if (line1 != ""):
				print "%s\n%s\n" %(line1, line2)
			else:
				print "\n"
			line1 = ""
			line2 = "#"
		line1 += " %s" %(tok.value)
		line2 += " %s" %(repr(tok.type))
	print "%s\n%s\n" %(line1, line2)

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runlexer(inputfile)
