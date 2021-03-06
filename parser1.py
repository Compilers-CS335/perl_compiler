import yacc

from lexer import tokens,lexer


# def p_start(p):
#     '''start : block
#              | statements'''


# def p_block(p):
# 	'block :BLOCK_BEGIN statements BLOCK_ENDS'
blockNUM = 0
blockbegNUM = 0
blockendNUM = 0
stmtsNUM = 0
emptyNUM = 0
stmtNUM = 0
switchstmtNUM = 0
switchNUM = 0
asgnNUM = 0
openparenthesisNUM =0
closeparenthesisNUM = 0
caselistNUM = 0
ifthenNUM = 0
ifNUM = 0


add = ""

def p_start(p):
    '''start : block
             | statements'''
    p[0] = "\tstart -- {" + p[1] + "};"

def p_block(p):
    'block : BLOCK_BEGIN  statements  BLOCK_ENDS'
    global blockNUM
    global add
    p[0] = "block_" +str(blockNUM)
    add += "\nblock_" +str(blockNUM)+ "-- {BLOCK_BEGIN_" +str(blockbegNUM)+ p[2] + "BLOCK_ENDS_" +str(blockendNUM)+ "};"


def p_statements(p):
    '''statements : statement statements
                  | statement empty'''

    global stmtsNUM
    stmtsNUM += 1
    p[0] = "statements_"+str(stmtsNUM)+" };\n statements_"+str(stmtsNUM)+" -- { " + p[1] +" " + p[2]



def p_empty(p):
    'empty :'
    global emptyNUM
    p[0] = "empty_" +str(emptyNUM)
    #add += "\nempty_" +str(emptyNUM)
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
                 | functionStetement 
                 | lastStatement
                 | nextStatement
                 | ifthen
                 | ifthenelse
                 | switchStatement
                 | ternaryStatement''' # implementinf ifthen and ifthenelse without nested loop
              

                 #    
                 # | loopcontrolStatement    
                 #      
                 #   
                 # 
                 # 
                 # | dowhileStatement
                 # | ternaryStatement 
                 # '''

    global stmtNUM
    global add
    stmtNUM += 1
    p[0] = "statement_" +str(stmtNUM);
    add += "\nstatement_" +str(stmtNUM)+ " -- {" + p[1] + "};"



def p_switchStatement(p):
	'switchStatement : SWITCH OPEN_PARANTHESIS lefthandside CLOSE_PARANTHESIS BLOCK_BEGIN caselist BLOCK_ENDS'
	global switchstmtNUM
	global switchNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	global blockbegNUM
	global blockendNUM
	global add
	switchstmtNUM +=1
	switchNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	blockbegNUM +=1
	blockendNUM +=1
	p[0] = "switchStatement_" +str(switchstmtNUM)
	add += "\nswitchStatement_" +str(switchstmtNUM)+ "-- { SWITCH_" +str(switchNUM)+ "OPEN_PARANTHESIS_" +str(openparenthesisNUM) + p[3] + "CLOSE_PARANTHESIS_" +str(closeparenthesisNUM)+ "BLOCK_BEGIN_" +str(blockbegNUM)+ p[6] + "BLOCK_ENDS_" +str(blockendNUM)+ "};"



def p_caselist(p):
    '''caselist : CASE OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block caselist
                | empty empty empty empty empty empty'''
    p[0] = "caselist_" +str(caselistNUM)
    add += "\ncaselist_" +str(caselistNUM)+ "-- { CASE_" +str(caseNUM)+ "OPEN_PARANTHESIS_" +str(openparenthesisNUM)+ p[3] + "CLOSE_PARANTHESIS_"  +str(closeparenthesisNUM)+ p[5] + p[6] + " };"
    #DOUBT HERE: CASE, EMPTY in the beginning


def p_caselistB(p):
	'caselistB : ELSE block'


def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block'
	global add
	global ifthenNUM
	global ifNUM
	ifthenNUM += 1
	ifNUM += 1
	p[0] = "ifthen_" + str(ifthenNUM);
	add += "\nifthen_" +str(ifthenNUM)+ " -- { IF ( " + p[3] + "then" + p[5] + " ) };"

def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block ELSE block'
	# global add
	# global ifthenelse
	# ifthenelse += 1
	# p[0] = "ifthenelse_" + str(ifthenelse)
	# add += "\nifthenelse_" +str(ifthenelse)+ " -- { IF OPEN_PARANTHESIS " + p[3] + " CLOSE_PARANTHESIS " + p[5] + " ELSE " + p[6] + "};" 


def p_lastStatement(p):
	'lastStatement : LAST SEMICOLON'
	# global add
	# global lastStatement
	# lastStatement += 1
	# p[0] = "lastStatement_" + str(lastStatement)
	# add += "\nlastStatement_" +str(lastStatement)+ " -- { LAST SEMICOLON };"

def p_nextStatement(p):
	'nextStatement : NEXT SEMICOLON'   # I am changing lexer here to accomodate this
	global add
	add += "\nnextStatement -- { NEXT STATEMENT };"



def p_functionStament(p):
	'functionStetement : SUB IDENTIFIER block'
	global add
	add += "\n"

def p_printStatement(p):
	'''printStatement : PRINT OPEN_PARANTHESIS string1 CLOSE_PARANTHESIS SEMICOLON
					  | PRINT empty string1 empty SEMICOLON'''

def p_string1(p):
	'''string1 : STRING
			   | RES_STRING'''

def p_return(p):
    'returnStatement : RETURN expression SEMICOLON'


def p_assignment(p):
    '''assignment : lefthandside decList empty assignmenttype expression SEMICOLON
                  | lefthandside decList CLOSE_PARANTHESIS assignmenttype expression SEMICOLON'''
    global asgnNUM
    global add
    asgnNUM = asgnNUM + 1
    p[0] = "assignment_"+str(asgnNUM)
    add += "assignment_"+str(asgnNUM)+" -- { LHS dec ass_type exp };"

def p_assignmenttype(p):
	'''assignmenttype : ADV_ASSIGNMENT_OP
					  | ASSIGNMENT_OP'''

def p_lefthandside(p):
	'''lefthandside : PRIVATE type
					| type
					| PRIVATE OPEN_PARANTHESIS type'''

def p_declaration(p):
	'''declaration :  lefthandside decList SEMICOLON
	               |   lefthandside decList CLOSE_PARANTHESIS SEMICOLON'''

def p_decList(p):
	'''decList :  COMMA type decList
	           |   empty'''



def p_functionCall(p):
	'functionCall : IDENTIFIER OPEN_PARANTHESIS parameters CLOSE_PARANTHESIS'

def p_parameters(p):
	'''parameters 	: expression COMMA parameters
					| expression
					| empty'''

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
def p_string(p):
	''' string 	: STRING 
				| RES_STRING'''

def p_number(p):
	''' number  : NUMBER
				| SCI_NOT
				| FLOAT
				| HEXADECIMAL
				| OCTAL'''
				#DOUBT, what to write here?

def p_variable(p):
	''' variable 	: VARIABLE 
					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET
					| VARIABLE BLOCK_BEGIN string BLOCK_ENDS'''
					#DOUBT

def p_term(p):
	''' term 	: number
				| type
				| variable
				| string
				| OPEN_PARANTHESIS term CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_01 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_02 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_03 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_04 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_05 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_06 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_07 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_08 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_09 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_10 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_11 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_12 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_13 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_14 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_15 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_16 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_17 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_18 CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_19 CLOSE_PARANTHESIS'''

def p_type(p):
	''' type : ARRAY
			 | HASH
			 | variable'''
					
#now we have finally got an expression for each term
# nonassoc    ++ --
def p_term_01(p):
	''' term_01	: term INCREMENT_OP
				| term DECREMENT_OP
				| INCREMENT_OP term
				| DECREMENT_OP term
				| term'''
# right   **
def p_term_02(p):
	''' term_02	: term_01 EXPONENT_OP term_02
				| term_01'''
# right   ! ~ \ and unary + and -				# our expressions will not have "\" in them .. it is for the strings
def p_term_03(p):
	''' term_03	: PLUS_OP term_02
				| MINUS_OP term_02
				| BIT_FLIP term_02
				| NOT_OP term_02
				| term_02'''
# left    =~ !~
def p_term_04(p):
	''' term_04	: term_04 SEARCH_MODIFY term_03
				| term_04 SEARCH_MODIFY_NEG term_03
				| term_03'''
# left    * / % x
def p_term_05(p):
	''' term_05	: term_05 MULTIPLICATION_OP term_04
				| term_05 DIVISION_OP term_04
				| term_05 MODULUS_OP term_04
				| term_05 REP_OP term_04
				| term_04'''
#     left    + - .
def p_term_06(p):
	''' term_06	: term_06 PLUS_OP term_05
				| term_06 MINUS_OP term_05
				| term_06 CONCATENATE term_05
				| term_05'''
#     left    << >>
def p_term_07(p):
	''' term_07	: term_07 BIT_RIGHT_SHIFT term_06
				| term_07 BIT_LEFT_SHIFT term_06
				| term_06'''
#     nonassoc    < > <= >= lt gt le ge
def p_term_08(p):
	''' term_08	: term_07 GREATER_OP term_07
				| term_07 LESS_OP term_07
				| term_07 GREATER_EQUAL_OP term_07
				| term_07 LESS_EQUAL_OP term_07
				| term_07'''
#     nonassoc    == != <=> eq ne cmp ~~ 		#not doing ~~
def p_term_09(p):
	''' term_09	: term_08 EQUALS_OP term_08
				| term_08 NOT_EQUALS_OP term_08
				| term_08 COMPARE_OP term_08
				| term_08'''
#     left    &
def p_term_10(p):
	''' term_10 : term_10 BIT_AND term_09
				| term_09'''
#     left    | ^
def p_term_11(p):
	''' term_11	: term_11 BIT_OR term_10
				| term_11 BIT_XOR term_10
				| term_10'''
#     left    &&
def p_term_12(p):
	''' term_12	: term_12 AND_OP term_11
				| term_11'''
#     left    || //								# // not implemented:: defined(EXPR1) ? EXPR1 : EXPR
def p_term_13(p):
	''' term_13	: term_13 OR_OP term_12
				| term_12'''


# nonassoc    ..  ... 							# not implemented ...
def p_term_14A(p):
	''' term_14A : term_13 RANGE_OP term_13'''


def p_term_14B(p):
	''' term_14B : term_13'''




# right   = += -= *= etc. goto last next redo dump		##### see if we can implement goto, last, next, redo ... dump not implemented
def p_term_15A(p):
	''' term_15A : term_14A ADV_ASSIGNMENT_OP term_15A
				| term_14A ADV_ASSIGNMENT_OP term_15B
				| term_14A ADV_ASSIGNMENT_OP term_15C
				| term_14B ADV_ASSIGNMENT_OP term_15A
				| term_14B ADV_ASSIGNMENT_OP term_15B
				| term_14B ADV_ASSIGNMENT_OP term_15C'''


def p_term_15B(p):
	''' term_15B : term_14A ASSIGNMENT_OP term_15A
				| term_14A ASSIGNMENT_OP term_15B
				| term_14A ASSIGNMENT_OP term_15C
				| term_14B ASSIGNMENT_OP term_15A
				| term_14B ASSIGNMENT_OP term_15B
				| term_14B ASSIGNMENT_OP term_15C'''


def p_term_15C(p):
	''' term_15C : term_14A
				| term_14B
				| term_14C'''



# left    , =>
def p_term_16A(p):
	''' term_16A : term_16A COMMA term_15A
				| term_16B COMMA term_15A
				| term_16C COMMA term_15A
				| term_16A COMMA term_15B
				| term_16B COMMA term_15B
				| term_16C COMMA term_15B
				| term_16A COMMA term_15C
				| term_16B COMMA term_15C
				| term_16C COMMA term_15C'''


def p_term_16B(p):
	'''term_16B	: term_16A ASSOCIATE_OP term_15A
				| term_16B ASSOCIATE_OP term_15A
				| term_16C ASSOCIATE_OP term_15A
				| term_16A ASSOCIATE_OP term_15B
				| term_16B ASSOCIATE_OP term_15B
				| term_16C ASSOCIATE_OP term_15B
				| term_16A ASSOCIATE_OP term_15C
				| term_16B ASSOCIATE_OP term_15C
				| term_16C ASSOCIATE_OP term_15C'''


def p_term_16C(p):
	''' term_16C	: term_15A
					| term_15B
					| term_15C'''



# right   not
def p_term_17A(p):
	'''term_17A : term_16A
				| term_16B
				| term_16C'''


def p_term_17B(p):
	'''term_17B : term_16A NOT_STR_OP term_17A
				| term_16A NOT_STR_OP term_17B
				| term_16B NOT_STR_OP term_17A
				| term_16B NOT_STR_OP term_17B
				| term_16C NOT_STR_OP term_17A
				| term_16C NOT_STR_OP term_17B''' 




# left    and
def p_term_18A(p):
	'''term_18A : term_17A 
				| term_17B'''

def p_term_18B(p):
	'''term_18B : term_18A AND_STR_OP term_17A
				| term_18B AND_STR_OP term_17A
				| term_18A AND_STR_OP term_17B
				| term_18B AND_STR_OP term_17B'''



# left    or xor
def p_term_19A(p):
	'''term_19A : term_18A
				| term_18B'''

def p_term_19B(p):
	''' term_19B : term_19A XOR_STR_OP term_18A
				| term_19B XOR_STR_OP term_18A
				| term_19C XOR_STR_OP term_18A
				| term_19A XOR_STR_OP term_18B
				| term_19B XOR_STR_OP term_18B
				| term_19C XOR_STR_OP term_18B'''

def p_term_19C(p):
	''' term_19C : term_19A OR_STR_OP term_18A
				| term_19B OR_STR_OP term_18A
				| term_19C OR_STR_OP term_18A
				| term_19A OR_STR_OP term_18B
				| term_19B OR_STR_OP term_18B
				| term_19C OR_STR_OP term_18B'''

#########temporary
def p_expression_number(p):
	''' expression 	: term_19A
					| term_19B
					| term_19C'''

##################################################
#ERROR HANDLING
##################################################
def p_error(p):
    # print "Temporary error statement! Has to be modified later"
    #panic mode recovery code
    print "Whoa. You are seriously in trouble."
    # Read ahead looking for a closing '}'
    # while True:
    #     tok = parser.token()             # Get the next token
    #     if not tok or tok.type == 'BLOCK_BEGIN' or tok.type == 'BLOCK_ENDS' or tok.type == 'SEMICOLON' : break
    # parser.errorok()
    # return tok



parser = yacc.yacc(debug=1)

def runparser(inputfile):
	program=open(inputfile).read()
	result=parser.parse(program,debug=1)
	result = "graph parse_tree {" + result + add + "}"
	print result 

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)






