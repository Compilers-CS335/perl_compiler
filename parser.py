import yacc

#get the token map from the lexer
from lexer import tokens

# start = expression

def p_expression(p):
	'expression : term PLUS_OP term SEMICOLON'
	p[0] = p[1] + p[3]

def p_term(p):
	'term : NUMBER'
	p[0] = p[1];

#error rule for syntax errors
def p_error(p):
	print "Syntax error in input!"

#Build the parser
parser = yacc.yacc()

while True:
	try:
		s = raw_input('calc > ')
	except EOFError:
		break
	if not s:continue
	result = parser.parse(s)
	print result