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
                  | statement empty'''
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
                 | forStatement   '''

                 #    
                 # | loopcontrolStatement    
                 #      
                 # 
                 # | ifThen  
                 # | ifThenElse  
                 # 
                 # 
                 # | dowhileStatement
                 # | ternaryStatement 
                 # | functionStetement'''





def p_return(p):
    'returnStatement : RETURN type SEMICOLON'


def p_assignment(p):
    'assignment : lefthandside assignmenttype expression SEMICOLON'

def p_assignmenttype(p):
	'''assignmenttype : ADV_ASSIGNMENT_OP
					  | ASSIGNMENT_OP'''

def p_lefthandside(p):
	'''lefthandside : PRIVATE type
					| type'''

def p_type(p):
	'''type : ARRAY
			| HASH
			| VARIABLE'''
					

def p_declaration(p):
    'declaration :  lefthandside decList SEMICOLON'

def p_decList(p):
	'''decList :  COMMA type decList
	           |   empty'''



def p_functionCall(p):
    'functionCall : IDENTIFIER OPEN_PARANTHESIS parameters CLOSE_PARANTHESIS'

def p_parameters(p):
    '''parameters : expression COMMA parameters
                  | expression
                  | empty'''

def p_while(p):
    'whileStatement : WHILE  OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  block'

def p_for(p):
    'forStatement : FOR  OPEN_PARANTHESIS expression SEMICOLON expression SEMICOLON expression CLOSE_PARANTHESIS  block'




#########temporary
def p_expression_number(p):
    'expression : NUMBER'

##################################################
#ERROR HANDLING
##################################################




parser = yacc.yacc(debug=1)

def runparser(inputfile):
	program=open(inputfile).read()
	result=parser.parse(program,debug=1)
	print result 

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)






