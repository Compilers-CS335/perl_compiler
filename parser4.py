import yacc

from lexer import tokens,lexer


# def p_start(p):
#     '''start : block
#              | statements'''


# def p_block(p):
# 	'block :BLOCK_BEGIN statements BLOCK_ENDS'



def p_start(p):
    '''start : block
             | statements'''






def p_block(p):
    'block : BLOCK_BEGIN  statements  BLOCK_ENDS'


    
def p_statments(p):
    '''statements : statement statements
                  | statement '''
   

def p_empty(p):
    'empty :'
    pass

# def p_empty_statements(p):
# 	'empty_statements : empty'

def p_statment(p):
    '''statement : assignment 
    		     | declaration 
                 | returnStatement 
                 | functionCall  
                 | whileStatement
                 | forStatement  
                 | printStatement
                 | functionStatement 
                 | lastStatement
                 | nextStatement
                 | ifthen
                 | ifthenelse
                 | useStatement
                 | switchStatement''' # implementinf ifthen and ifthenelse without nested loop

                 #    
                 # | loopcontrolStatement    
                 #      
                 #   
                 # 
                 # 
                 # | dowhileStatement
                 # | ternaryStatement 
                 # '''
    


def p_useStatement(p):
	'useStatement : USE IDENTIFIER SEMICOLON'
	
def p_switchStatement(p):
	'switchStatement : SWITCH lefthandside  BLOCK_BEGIN caselist BLOCK_ENDS'
	


def p_caselist(p):
    '''caselist : CASE OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block caselist
    			| ELSE  block 
                | empty '''
    

def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block'
	


def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block ELSE block'
	

def p_lastStatement(p):
	'lastStatement : LAST SEMICOLON'
	

def p_nextStatement(p):
	'nextStatement : NEXT SEMICOLON'
	
def p_functionStament(p):
	'functionStatement : SUB IDENTIFIER block'
	
def p_printStatement(p):
	'''printStatement : PRINT OPEN_PARANTHESIS string1 CLOSE_PARANTHESIS SEMICOLON
						| PRINT  string1  SEMICOLON
						| PRINT  expression  SEMICOLON'''
	
def p_string1(p):
	'''string1 : STRING
			   | RES_STRING'''
	
def p_return(p):
    'returnStatement : RETURN expression SEMICOLON'
    

def p_assignment(p):
    'assignment : lefthandside assignmenttype expression SEMICOLON'
    

def p_assignmenttype(p):
	'''assignmenttype : ADV_ASSIGNMENT_OP
					  | ASSIGNMENT_OP'''
	

def p_lefthandside(p):
	'''lefthandside : PRIVATE type decList 
					| PRIVATE OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
	
def p_lefthandsided(p):
	'''lefthandside : LOCAL  type decList 
					| LOCAL OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
	
def p_lefthandsideb(p):
	'''lefthandside : OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
	

def p_lefthandsidec(p):
	'lefthandside : type'
	


def p_declaration(p):
	'declaration :  lefthandside SEMICOLON'
	
def p_decList(p):
	'''decList :  COMMA type decList
	           |  empty'''
	



def p_functionCall(p):
	'functionCall : IDENTIFIER OPEN_PARANTHESIS parameters CLOSE_PARANTHESIS SEMICOLON' 
	

def p_parameters(p):
	'''parameters 	: expression COMMA parameters
					| expression 
					| empty '''
					#### KAISE START KARU. SPLIT KARNA PADEGA
	
def p_while(p):
	'whileStatement : WHILE  OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  block'
	

def p_for(p):
	'forStatement : FOR  OPEN_PARANTHESIS expression SEMICOLON expression SEMICOLON expression CLOSE_PARANTHESIS  block'
	

### EXPRESSIONS
	# associativity and precedence
	# left    terms and list operators (leftward)
	# left    ->									# we are not implementing this
	# nonassoc    ++ --
	# right   **
	# right   ! ~ \ and unary + and -				# \ not required
	# left    =~ !~
	# left    * / % x
	#     left    + - .
	#     left    << >>
	#     nonassoc    named unary operators			#-------------------
	#     nonassoc    < > <= >= lt gt le ge
	#     nonassoc    == != <=> eq ne cmp ~~		# we had not implemented ~~ in lexer.. leaving for now
	#     left    &
	#     left    | ^
	#     left    &&
	#     left    || //								# // not implemented:: defined(EXPR1) ? EXPR1 : EXPR
	# nonassoc    ..  ... 							# not implemented ...
	# right   ?:									# -------------------
	# right   = += -= *= etc. goto last next redo dump		##### see if we can implement goto, last, next, redo ... dump not implemented
	# left    , =>
	# nonassoc    list operators (rightward)		#---------------------
	# right   not
	# left    and
	# left    or xor

precedence = (
	('left', 'OR_STR_OP', 'XOR_STR_OP'),
	('left', 'AND_STR_OP'),
	('right', 'NOT_STR_OP'),
	('left', 'COMMA', 'ASSOCIATE_OP'),
	('right', 'ADV_ASSIGNMENT_OP', 'ASSIGNMENT_OP'),
	('nonassoc', 'RANGE_OP'),
	('left', 'OR_OP'),
	('left', 'AND_OP'),
	('left', 'BIT_OR', 'BIT_XOR'),
	('left', 'BIT_AND'),
	('nonassoc', 'EQUALS_OP', 'NOT_EQUALS_OP', 'COMPARE_OP'),
	('nonassoc', 'GREATER_OP', 'LESS_OP', 'GREATER_EQUAL_OP', 'LESS_EQUAL_OP'),
	('left', 'BIT_RIGHT_SHIFT', 'BIT_LEFT_SHIFT'),
	('left', 'PLUS_OP', 'MINUS_OP', 'CONCATENATE'),
	('left', 'MULTIPLICATION_OP', 'DIVISION_OP', 'MODULUS_OP', 'REP_OP'),
	('left', 'SEARCH_MODIFY', 'SEARCH_MODIFY_NEG'),
	('right', 'UPLUS', 'UMINUS', 'BIT_FLIP', 'NOT_OP'),
	('right', 'EXPONENT_OP'),
	('nonassoc', 'INCREMENT_OP', 'DECREMENT_OP'),
)

def p_string(p):
	''' string 	: STRING 
				| RES_STRING'''
	
def p_number(p):
	''' number  : NUMBER
				| SCI_NOT
				| FLOAT
				| HEXADECIMAL
				| OCTAL'''
	

#SPLIT
# def p_variableA(p):
# 	''' variableA 	: VARIABLE  empty empty empty
# 					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET'''  ### Ye Bracket hai ya parenthesis???

def p_variable(p):
	'''variable : VARIABLE  
					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET
					| VARIABLE BLOCK_BEGIN string BLOCK_ENDS'''
	


def p_term(p):
	''' term 	:  number 
				|  type 
				|  variable 
				|  string  
				| OPEN_PARANTHESIS expression CLOSE_PARANTHESIS'''
	


def p_type(p):
	''' type : ARRAY
			 | HASH'''
	
def p_type1(p):
	' type : variable'
	

def p_expression_unary(p):
	''' expression : PLUS_OP expression   %prec UPLUS
				   | MINUS_OP expression  %prec UMINUS
				   | BIT_FLIP expression
				   | NOT_OP expression
				   | INCREMENT_OP expression
				   | DECREMENT_OP expression'''
	
def p_expression(p):
	''' expression : expression INCREMENT_OP
				   | expression DECREMENT_OP'''
	

def p_expression_empty(p):
	'expression : empty'
	

def p_expression_term(p):
	'expression : term'
	


def p_expression_binary(p):
	'''expression : expression OR_STR_OP expression
				  | expression XOR_STR_OP expression
				  | expression AND_STR_OP expression
				  | expression NOT_STR_OP expression
				  | expression COMMA expression
				  | expression ASSOCIATE_OP expression
				  | expression ADV_ASSIGNMENT_OP expression
				  | expression ASSIGNMENT_OP expression
				  | expression RANGE_OP expression
				  | expression OR_OP expression
				  | expression AND_OP expression
				  | expression BIT_OR expression
				  | expression BIT_XOR expression
				  | expression BIT_AND expression
				  | expression EQUALS_OP expression
				  | expression NOT_EQUALS_OP expression
				  | expression COMPARE_OP expression
				  | expression GREATER_OP expression
				  | expression LESS_OP expression
				  | expression GREATER_EQUAL_OP expression
				  | expression LESS_EQUAL_OP expression
				  | expression BIT_RIGHT_SHIFT expression
				  | expression BIT_LEFT_SHIFT expression
				  | expression PLUS_OP expression
				  | expression MINUS_OP expression
				  | expression CONCATENATE expression
				  | expression MULTIPLICATION_OP expression
				  | expression DIVISION_OP expression
				  | expression MODULUS_OP expression
				  | expression REP_OP expression
				  | expression SEARCH_MODIFY expression
				  | expression SEARCH_MODIFY_NEG expression
				  | expression EXPONENT_OP expression'''
	







##################################################
#ERROR HANDLINGva
##################################################
def p_error(p):
	print "ERROR IN PARSING PHASE!!!"
	#panic mode recovery code



parser = yacc.yacc(debug=1)

def runparser(inputfile):
	program=open(inputfile).read()
	result=parser.parse(program,debug=1)
	print result 

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)