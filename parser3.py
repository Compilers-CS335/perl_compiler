import yacc

from lexer import tokens,lexer


# def p_start(p):
#     '''start : block
#              | statements'''


# def p_block(p):
# 	'block :BLOCK_BEGIN statements BLOCK_ENDS'
add = ""

stmtsNUM = 0
stmtNUM = 0
asgnNUM = 0

blockbeginNUM = 0
blockcloseNUM = 0


def p_start(p):
    '''start : block
             | statements'''
    p[0] = "\tstart -- {" + p[1] + "};"

def p_block(p):
    'block : BLOCK_BEGIN  statements  BLOCK_ENDS'
    p[0] = "block"
    global add
    global blockcloseNUM
    global blockbeginNUM
    add += "\nblock -- { " + "BLOCK_BEGIN" + "_" +str(blockbeginNUM) + " " + p[2] + " BLOCK_ENDS" + "_" +str(blockcloseNUM)+ " };"

def p_statments(p):
    '''statements : statement statements
                  | statement empty
                  | empty empty'''
    global stmtsNUM
    stmtsNUM = stmtsNUM + 1
    p[0] = "statements_"+str(stmtsNUM)+" };\n statements_"+str(stmtsNUM)+" -- { " + p[1] +" " + p[2]


def p_empty(p):
    'empty :'
    p[0] = "empty"
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
                 | ifthenelse''' # implementinf ifthen and ifthenelse without nested loop

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
    stmtNUM = stmtNUM + 1
    p[0] = "statement_"+str(stmtNUM);
    add += "\nstatement_"+str(stmtNUM)+" -- {" + p[1] + "};"

def p_switchStatement(p):
	'switchStatement : SWITCH OPEN_PARANTHESIS lefthandside CLOSE_PARANTHESIS BLOCK_BEGIN caselist BLOCK_ENDS'
	global switchstmtNUM
	global switchNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	global blockbegNUM
	global blockcloseNUM
	global add
	switchstmtNUM +=1
	switchNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	blockbeginNUM +=1
	blockcloseNUM +=1
	p[0] = "switchStatement_" +str(switchstmtNUM)
	add += "\nswitchStatement_" +str(switchstmtNUM)+ "-- { SWITCH_" +str(switchNUM)+ p[2] + "_" +str(openparenthesisNUM) + p[3] + " " + p[4] + "_" +str(closeparenthesisNUM)+ "BLOCK_BEGIN_" +str(blockbeginNUM)+ p[6] + "BLOCK_ENDS_" +str(blockcloseNUM)+ "};"


def p_caselist(p):
    '''caselist : CASE OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block caselist
    			| ELSE empty empty empty block empty
                | empty empty empty empty empty empty'''
    global add
    global caselistNUM
    global caseNUM
    global openparenthesisNUM
    global closeparenthesisNUM
	caselistNUM +=1
	caseNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
    p[0] = "caselist_" +str(caselistNUM)
    add += "\ncaselist_" +str(caselistNUM)+ "-- { " +p[1]+ "_" +str(caseNUM)+ p[2] + "_" +str(openparenthesisNUM)+ p[3] + " " + p[4] + "_" +str(closeparenthesisNUM)+ p[5] + " " + p[6] + " };"


def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block'
	global add
	global ifthenNUM
	global ifNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	ifthenNUM += 1
	openparenthesisNUM += 1
	closeparenthesisNUM += 1
	ifNUM += 1
	p[0] = "ifthen_" + str(ifthenNUM);
	add += "\nifthen_" +str(ifthenNUM)+ " -- { IF_" +str(ifNUM) + p[2] + "_" +str(openparenthesisNUM)+ p[3] + " " + p[4] + "_" +str(closeparenthesisNUM) + p[5] + " };"


def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block ELSE block'
	global add
	global ifthenelse
	global openparenthesisNUM
	global closeparenthesisNUM
	global caseNUM
	ifthenelse += 1
	ifNUM +=1
	openparenthesisNUM += 1
	closeparenthesisNUM += 1
	caseNUM += 1
	p[0] = "ifthenelse_" + str(ifthenelse)
	add += "\nifthenelse_" +str(ifthenelse)+ " -- { IF_" +str(ifNUM) +p[2] + "_" +str(openparenthesisNUM)+ p[3] + " " + p[4] + "_" +str(closeparenthesisNUM) + p[5] + " ELSE_" +str(caseNUM) + p[6] + "};" 


def p_lastStatement(p):
	'lastStatement : LAST SEMICOLON'
	global add
	global lastStatement
	global lastNUM
	global semicolonNUM
	lastStatement += 1
	lastNUM +=1
	semicolonNUM +=1
	p[0] = "lastStatement_" + str(lastStatement)
	add += "\nlastStatement_" +str(lastStatement)+ " -- { LAST_" +str(lastNUM)+ " SEMICOLON_" +str(semicolonNUM)+ " };"


def p_nextStatement(p):
	'nextStatement : NEXT SEMICOLON'
	global add
	global nextStatement
	global nextNUM
	global semicolonNUM
	nextStatement +=1
	nextNUM +=1
	semicolonNUM +=1
	p[0] = "nextStatement_" + str(nextStatement)
	add += "\nnextStatement_" +str(nextStatement)+ " -- { NEXT_" +str(nextNUM)+ " SEMICOLON_" +str(semicolonNUM)+ " };"
	   # I am changing lexer here to accomodate this

def p_functionStament(p):
	'functionStatement : SUB IDENTIFIER block'
	global add
	global functionStatementNUM
	global subNUM
	global identifierNUM
	functionStatement += 1
	subNUM += 1
	identifierNUM +=1
	p[0] = "functionStatement_" + str(functionStatementNUM)
	add += "\nfunctionStatement_" + str(functionStatementNUM)+ " -- { SUM_" +str(subNUM)+ "IDENTIFIER_" +str(identifierNUM)+ p[3] + " };"

def p_printStatement(p):
	'printStatement : PRINT OPEN_PARANTHESIS string1 CLOSE_PARANTHESIS SEMICOLON'
	global add
	global printstatementNUM
	global printNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	global semicolonNUM
	printstatementNUM +=1
	printNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	semicolonNUM +=1
	p[0] = "printStatement_" + str(printstatementNUM)
	add += "\nprintStatement_" + str(printstatementNUM)+ " -- { PRINT_" +str(printNUM)+ p[2] + "_" +str(openparenthesisNUM) + p[3] + p[4] + "_" +str(closeparenthesisNUM)+ "SEMICOLON_" +str(semicolonNUM)+ " };"

def p_string1(p):
	'''string1 : STRING
			   | RES_STRING'''
	global add
	global string1NUM
	global strinNUM
	string1NUM +=1
	strinNUM +=1
	p[0] = "string1_" + str(string1NUM)
	add += "\nstring1_" + str(string1NUM)+ " -- { " + p[1] + "_" +str(strinNUM)+ " };"

def p_return(p):
    'returnStatement : RETURN expression SEMICOLON'
    global add
    global returnstmtNUM
    global returnNUM
    global semicolonNUM
    returnstmtNUM +=1
    returnNUM +=1
    semicolonNUM +=1
    p[0] = "returnStatement_" + str(returnstmtNUM)
    add += "\nreturnStatement_" + str(returnstmtNUM)+ " -- { RETURN_" +str(returnNUM)+ p[2] + "SEMICOLON_" + str(semicolonNUM) + " };"


def p_assignment(p):
    '''assignment : lefthandside decList  empty assignmenttype expression SEMICOLON
                  | lefthandside decList CLOSE_PARANTHESIS assignmenttype expression SEMICOLON'''
    global asgnNUM
    global closeparenthesisNUM
    global semicolonNUM
    global add
    closeparenthesisNUM +=1
    semicolonNUM +=1
    asgnNUM += 1
    p[0] = "assignment_" +str(asgnNUM)
    add += "\nassignment_" +str(asgnNUM)+ " -- { " + p[1] + p[2] + p[3] + "_" +str(closeparenthesisNUM)+ p[4] + p[5] + "SEMICOLON_" + str(semicolonNUM) + " };"


def p_assignmenttype(p):
	'''assignmenttype : ADV_ASSIGNMENT_OP
					  | ASSIGNMENT_OP'''
	global add
	global assntypeNUM
	global assntypeopNUM
	assntypeopNUM +=1
	assntypeNUM +=1
	p[0] = "assignmenttype_" +str(assntypeNUM)
	add += "\nassignmenttype_" +str(assntypeNUM)+ " -- { " +p[1]+ "_" +str(assntypeopNUM)+ " };"


def p_lefthandside(p):
	'''lefthandside : PRIVATE  empty type
					| empty empty type 
					| PRIVATE OPEN_PARANTHESIS type'''
	global add
	global lefthandsideNUM
	global privateNUM
	global openparenthesisNUM
	lefthandside +=1
	privateNUM +=1
	openparenthesisNUM +=1
	p[0] = "lefthandside_" +str(lefthandsideNUM)
	add += "\nlefthandside_" +str(lefthandsideNUM)+ " -- { " +p[1]+ "_" +str(privateNUM)+ p[2] +"_" +str(openparenthesisNUM)+ p[3] + " };"




def p_declaration(p):
	'''declaration :  lefthandside decList  empty SEMICOLON
	               |   lefthandside decList CLOSE_PARANTHESIS SEMICOLON'''
	global add
	global declarationNUM
	global closeparenthesisNUM
	global semicolonNUM
	declarationNUM +=1
	closeparenthesisNUM +=1
	semicolonNUM +=1
	p[0] = "declaration_" +str(declarationNUM)
	add += "\ndeclaration_" +str(declarationNUM)+ " -- { " +p[1]+ p[2] + p[3]+ "_" +str(closeparenthesisNUM)+ "SEMICOLON_" + str(semicolonNUM) + " };"


def p_decList(p):
	'''decList :  COMMA type decList
	           |   empty  empty  empty'''
	global add
	p[0] = "declist_" +str(declistNUM)
	add += "\ndeclist_" +str(declistNUM)  ### ??? KAISE LIKHU AAGE?? Split karna padega




def p_functionCall(p):
	'functionCall : IDENTIFIER OPEN_PARANTHESIS parameters CLOSE_PARANTHESIS'
	global add
	global functncallNUM
	global identifierNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	functncallNUM +=1
	identifierNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	p[0] = "functionCall_" +str(functncallNUM)
	add += "\nfunctionCall_" +str(functncallNUM) + p[1] + "_" +str(identifierNUM)+ p[2] + "_" +str(openparenthesisNUM)+ p[3] + p[4] + "_" +str(closeparenthesisNUM) + " };"


def p_parameters(p):
	'''parameters 	: expression COMMA parameters
					| expression  empty  empty
					| empty  empty  empty'''
					#### KAISE START KARU. SPLIT KARNA PADEGA

def p_while(p):
	'whileStatement : WHILE  OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  block'
	global add
	global whilestmtNUM
	global whileNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	whilestmtNUM +=1
	whileNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	p[0] = "whileStatement_" +str(whilestmtNUM)
	add += "\nwhileStatement_" +str(whilestmtNUM)+ p[1] + "_" +str(whileNUM) + p[2] + "_" +str(openparenthesisNUM)+ p[3] + p[4]+ "_" +str(closeparenthesisNUM)+ p[5]


def p_for(p):
	'forStatement : FOR  OPEN_PARANTHESIS expression SEMICOLON expression SEMICOLON expression CLOSE_PARANTHESIS  block'
	global add
	p[0] = "forStatement_" +str(forstmtNUM)
	add  += "\nforStatement_" +str(forstmtNUM)+ " -- { FOR_" +str(forNUM)+ "OPEN_PARANTHESIS_" +str(openparenthesisNUM)+ p[3] + "SEMICOLON_" + str(semicolonNUM) + p[4] +  
	#### KYA KARU 2 SEMICOLON KA???

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
	global add
	global strngNUM
	strngNUM +=1
	p[0] = "string_" + str(strngNUM)
	add += "\nstring_" + str(strngNUM) + " -- { " + p[1] + " };"

def p_number(p):
	''' number  : NUMBER
				| SCI_NOT
				| FLOAT
				| HEXADECIMAL
				| OCTAL'''
	global add
	global numberNUM += 1
	p[0] = "number_" + str(numberNUM)
	add += "\nnumber_" + str(numberNUM) + " -- { " + p[1] + " };"


#SPLIT
def p_variableA(p):
	''' variableA 	: VARIABLE  empty empty empty
					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET'''  ### Ye Bracket hai ya parenthesis???

def p_variableB(p):
	'variableB : VARIABLE BLOCK_BEGIN string BLOCK_ENDS'
	global add
	global variblebNUM
	global blockbeginNUM
	global blockcloseNUM
	variblebNUM +=1
	blockcloseNUM +=1
	blockbeginNUM +=1
	p[0] = "variableB_" + str(variblebNUM)
	add += "\nvariableB_" +str(variblebNUM)+ " -- { " + p[1] + "BLOCK_BEGIN_" +str(blockbeginNUM)+ p[3] + "BLOCK_ENDS_" + str(blockcloseNUM) + " };"



def p_term(p):
	''' term 	: empty number empty
				| empty type empty
				| empty variableA empty
				| empty variableB empty
				| empty string  empty
				| OPEN_PARANTHESIS term CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_01A CLOSE_PARANTHESIS
				| OPEN_PARANTHESIS term_01B CLOSE_PARANTHESIS
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
	global add
	global termNUM
	global openparenthesisNUM
	global closeparenthesisNUM
	termNUM +=1
	openparenthesisNUM +=1
	closeparenthesisNUM +=1
	p[0] = "term_" + str(termNUM)
	add += "\nterm_" + str(termNUM)+ " -- { " + p[1] + "_" + str(openparenthesisNUM) + p[2] + p[3] + "_" + str(closeparenthesisNUM) + " };" 


def p_type(p):
	''' type : ARRAY
			 | HASH
			 | variableA
			 | variableB'''
	global add
	global typeNUM
	typeNUM +=1
	p[0] = "type_" + str(typeNUM)
	add += "\ntype_" + str(typeNUM) + " -- { " + p[1] + " };"
					
#now we have finally got an expression for each term
# nonassoc    ++ --
#SPLIT
def p_term_01A(p):
	''' term_01A : INCREMENT_OP term
				| DECREMENT_OP term
				| empty term_01A'''

def p_term_01B(p):
	''' term_01B : INCREMENT_OP term
				| DECREMENT_OP term
				| empty term'''

# right   **
def p_term_02(p):
	''' term_02	: term_01A EXPONENT_OP term_02
				| term_01A  empty empty
				| term_01B EXPONENT_OP term_02
				| term_01B  empty empty'''
# right   ! ~ \ and unary + and -				# our expressions will not have "\" in them .. it is for the strings
def p_term_03(p):
	''' term_03	: PLUS_OP term_02
				| MINUS_OP term_02
				| BIT_FLIP term_02
				| NOT_OP term_02
				| empty term_02'''
# left    =~ !~
def p_term_04(p):
	''' term_04	: term_04 SEARCH_MODIFY term_03
				| term_04 SEARCH_MODIFY_NEG term_03
				| term_03 empty empty'''
# left    * / % x
def p_term_05(p):
	''' term_05	: term_05 MULTIPLICATION_OP term_04
				| term_05 DIVISION_OP term_04
				| term_05 MODULUS_OP term_04
				| term_05 REP_OP term_04
				| term_04 empty empty'''
#     left    + - .
def p_term_06(p):
	''' term_06	: term_06 PLUS_OP term_05
				| term_06 MINUS_OP term_05
				| term_06 CONCATENATE term_05
				| term_05 empty empty'''
#     left    << >>
def p_term_07(p):
	''' term_07	: term_07 BIT_RIGHT_SHIFT term_06
				| term_07 BIT_LEFT_SHIFT term_06
				| term_06 empty empty'''
#     nonassoc    < > <= >= lt gt le ge
def p_term_08(p):
	''' term_08	: term_07 GREATER_OP term_07
				| term_07 LESS_OP term_07
				| term_07 GREATER_EQUAL_OP term_07
				| term_07 LESS_EQUAL_OP term_07
				| term_07 empty empty'''
#     nonassoc    == != <=> eq ne cmp ~~ 		#not doing ~~
def p_term_09(p):
	''' term_09	: term_08 EQUALS_OP term_08
				| term_08 NOT_EQUALS_OP term_08
				| term_08 COMPARE_OP term_08
				| term_08 empty empty'''
#     left    &
def p_term_10(p):
	''' term_10 : term_10 BIT_AND term_09
				| term_09 empty empty'''
#     left    | ^
def p_term_11(p):
	''' term_11	: term_11 BIT_OR term_10
				| term_11 BIT_XOR term_10
				| term_10 empty empty'''
#     left    &&
def p_term_12(p):
	''' term_12	: term_12 AND_OP term_11
				| term_11 empty empty'''
#     left    || //								# // not implemented:: defined(EXPR1) ? EXPR1 : EXPR
def p_term_13(p):
	''' term_13	: term_13 OR_OP term_12
				| term_12 empty empty'''
# nonassoc    ..  ... 							# not implemented ...
def p_term_14(p):
	''' term_14 : term_13 RANGE_OP term_13
				| term_13 empty empty'''
# right   = += -= *= etc. goto last next redo dump		##### see if we can implement goto, last, next, redo ... dump not implemented
def p_term_15(p):
	''' term_15 : term_14 ADV_ASSIGNMENT_OP term_15
				| term_14 ASSIGNMENT_OP term_15
				| term_14 empty empty'''
# left    , =>
def p_term_16(p):
	''' term_16	: term_16 COMMA term_15
				| term_16 ASSOCIATE_OP term_15
				| term_15 empty empty'''
# right   not
def p_term_17(p):
	''' term_17 : term_16 NOT_STR_OP term_17
				| term_16 empty empty'''
# left    and
def p_term_18(p):
	''' term_18 : term_18 AND_STR_OP term_17
				| term_17 empty empty'''
# left    or xor
def p_term_19(p):
	''' term_19 : term_19 OR_STR_OP term_18
				| term_19 XOR_STR_OP term_18
				| term_18 empty empty'''

#########temporary
def p_expression_number(p):
	'''expression : term_19
	              | term'''



##################################################
#ERROR HANDLING
##################################################
def p_error(p):
	print "Temporary error statement! Has to be modified later"
	#panic mode recovery code



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