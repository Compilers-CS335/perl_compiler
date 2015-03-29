import yacc
import symbolTable
import tac

from lexer import tokens,lexer


# def p_start(p):
#     '''start : block
#              | statements'''


# def p_block(p):
# 	'block :BLOCK_BEGIN statements BLOCK_ENDS'

symTable = symbolTable.SymbolTable()
threeAddrCode = tac.Tac(symTable)

def p_start(p):
    '''start : block
             | statements'''

    p[0] = p[1]
    

def p_block(p):
    'block : BLOCK_BEGIN  statements  BLOCK_ENDS'

    p[0] = p[2]
    
def p_statments(p):
    'statements : statement statements'

def p_statments_single(p):
	'statements : statement '

	p[0] = p[1]

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
    p[0] = p[1]


def p_useStatement(p):
	'useStatement : USE IDENTIFIER SEMICOLON'
	
def p_switchStatement(p):
	'switchStatement : SWITCH lefthandside  BLOCK_BEGIN caselist BLOCK_ENDS'
	


def p_caselist(p):
    '''caselist : CASE OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block caselist
    			| ELSE  block 
                | empty '''
    

def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerif block'

	if p[3]['type']!="BOOLEAN":
		print "Expression is not bool"

	p[0]['beginlist']=p[6].get('beginlist',[])
	p[0]['endlist']=p[6].get('endlist',[])
	p[0]={'nextlist': threeAddrCode.merge(p[5].get('falselist',[]),p[6].get('nextlist',[]))}	


def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  Markerif block ELSE Markerelse block'

	if p[3]['type']!="BOOLEAN":
		print "Expression is not bool"

	p[0]['beginlist']=threeAddrCode.merge( p[6].get('beginlist',[]), p[9].get('beginlist',[]))}
	p[0]['endlist']=threeAddrCode.merge( p[6].get('endlist',[]), p[9].get('endlist',[]))}

	threeAddrCode.backpatch(p[5]['falselist'],p[8]['quad'])
	p[0]={'nextlist' : p[8]['nextlist']}

def p_Markerif(p):
	p[0]={'falselist' : threeAddrCode.pointer_quad_next()}
	threeAddrCode.emit(p[-2]['place'], '','GOTO_MARK','-1')

def p_Markerelse(p):
	p[0]={'nextlist' : threeAddrCode.pointer_quad_next()}
	threeAddrCode.emit('', '','GOTO','-1')	
	

def p_lastStatement(p):
	'lastStatement : LAST SEMICOLON'
	p[0]={'endlist' : threeAddrCode.pointer_quad_next()}
	threeAddrCode.emit('','','GOTO','-1')

def p_nextStatement(p):
	'nextStatement : NEXT SEMICOLON'
	p[0]={'beginlist' : threeAddrCode.pointer_quad_next()}
	threeAddrCode.emit('','','GOTO','-1')


	




def p_functionStament(p):
	'functionStatement : SUB IDENTIFIER block'
	
def p_printStatement(p):
	'printStatement : PRINT OPEN_PARANTHESIS expression CLOSE_PARANTHESIS SEMICOLON'

def p_printStatement_no_paran(p):
	'printStatement : PRINT  expression  SEMICOLON'

	p[0] = {'place':symTable.newtmp()}
	if p[2]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		exp_type = "VOID"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type']=exp_type 
					
	
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
	'whileStatement : WHILE Marker OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerwhile  block'
	
	p[0]={'nextlist':[],'type' : 'VOID'}

	if p[4]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[7]['beginlist'],p[2]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[7].get('endlist',[]),p[7].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[6].get('falselist',[]),p[0].get('nextlist',[]))
		threeAddrCode.emit('','','GOTO',p[2]['quad'])
	else:
		print "Expression not bool"

def p_Markerwhile(p):
	'Markerwhile : empty'
	p[0]={'falselist' : threeAddrCode.pointer_quad_next()}
	threeAddrCode.emit(p[-2]['place'],'','GOTO_MARK','-1')

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
	'string : STRING'

	p[0] = {'type':'STRING', 'place':p[1]}

def p_res_string(p):
	'string : RES_STRING'

	p[0] = {'type':'RES_STRING', 'place':p[1]}
	
def p_number(p):
	''' number  : NUMBER
				| SCI_NOT
				| FLOAT
				| HEXADECIMAL
				| OCTAL'''

	p[0] = {'type':'NUMBER', 'place':p[1]}

#SPLIT
# def p_variableA(p):
# 	''' variableA 	: VARIABLE  empty empty empty
# 					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET'''  ### Ye Bracket hai ya parenthesis???

def p_variable(p):
	'''variable : VARIABLE
				| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET'''
	
	p[0] = {'place':p[1]}

def p_term(p):
	''' term 	:  number 
				|  type 
				|  string  '''

	p[0] = p[1]

def p_term_exp(p):
	'term : OPEN_PARANTHESIS expression CLOSE_PARANTHESIS'

	p[0] = p[2]

def p_type_var(p):
	'type : variable'

	p[0] = p[1]

####
def p_type(p):
	' type : ARRAY'

def p_expression_unary(p):								#INCREMENT_OP and DECREMENT_OP deleted
	''' expression : PLUS_OP expression   %prec UPLUS
				   | MINUS_OP expression  %prec UMINUS
				   | BIT_FLIP expression'''

	p[0] = {'place':symTable.newtmp()}

	if p[2]['type']!='NUMBER' :
		print "ERROR: Type error.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "NUMBER"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type']= exp_type 

def p_expression_unary_notOp(p):
	'expression : NOT_OP expression'
	
	p[0] = {'place':symTable.newtmp(), 'truelist':p[2]['falselist'], 'falselist':p[2]['truelist']}
	if p[2]['type']!='BOOLEAN' :
		print "ERROR: Type error in expression.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type'] = exp_type

# def p_expression(p):
# 	''' expression : expression INCREMENT_OP
# 				   | expression DECREMENT_OP'''
# 	if p[1]['type']!='NUMBER' :
# 		print "ERROR: Type error.\n"
# 		exp_type = "TYPE ERROR"
# 	else:
# 		exp_type = "NUMBER"
# 	p[0] = {'type' : exp_type, 'place':symTable.newtmp()}
	

def p_expression_empty(p):
	'expression : empty'
	

def p_expression_term(p):
	'expression : term'

	p[0] = p[1]
	
## SAB KUCHH ACHCHHE SE DEKHO ISME
def p_expression_bin_dig(p):
	'''expression : expression OR_STR_OP expression
					| expression XOR_STR_OP expression
					| expression AND_STR_OP expression
					| expression NOT_STR_OP expression
					| expression COMPARE_OP expression
					| expression BIT_OR expression
					| expression BIT_XOR expression
					| expression BIT_AND expression'''

def p_exp_and_op(p):
	'expression : expression AND_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'falselist':threeAddrCode.merge(p[1]['falselist'], p[4]['falselist']), 'truelist':p[4]['truelist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "ERROR: Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['truelist'], p[3]['quad'])
	p[0]['type']=exp_type

def p_exp_or_op(p):
	'expression : expression OR_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'truelist':threeAddrCode.merge(p[1]['truelist'], p[4]['truelist']), 'falselist':p[4]['falselist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "ERROR: Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['falselist'], p[3]['quad'])
	p[0]['type']=exp_type

def p_expression_binary_relational(p):
	'''expression : expression EQUALS_OP expression
				  | expression NOT_EQUALS_OP expression
				  | expression GREATER_OP expression
				  | expression LESS_OP expression
				  | expression GREATER_EQUAL_OP expression
				  | expression LESS_EQUAL_OP expression'''

	if p[1]['type']!='NUMBER' or p[3]['type']!='NUMBER' :
		print "ERROR: cannot compare\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"

	p[0] = {'type' : exp_type, 'place':symTable.newtmp(), 'truelist':[threeAddrCode.pointer_quad_next()], 'falselist':[1+threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

def p_marker_relational(p):
	'Marker : empty'

	p[0] = {'quad': threeAddrCode.pointer_quad_next()}

def p_expression_math(p):
	'''expression 	: expression PLUS_OP expression
					| expression MINUS_OP expression
					| expression MULTIPLICATION_OP expression
					| expression DIVISION_OP expression
					| expression MODULUS_OP expression
					| expression EXPONENT_OP expression
					| expression BIT_RIGHT_SHIFT expression
					| expression BIT_LEFT_SHIFT expression'''

	p[0] = {'place':symTable.newtmp()}
	if p[1]['type']!='NUMBER' or p[3]['type']!='NUMBER' :
		print "ERROR: cannot perform operation\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "NUMBER"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type


def p_expression_concat(p):
	'expression : expression CONCATENATE expression'

	p[0] = {'place':symTable.newtmp()}
	if p[1]['type']!='STRING' or p[3]['type']!='STRING' :
		print "ERROR: Concatenation operation works only on strings\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = 'STRING'
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type

def p_expression_repeatition(p):
	'expression : expression REP_OP expression'

 	p[0] = {'place':symTable.newtmp()}
	if p[3]['type']!='NUMBER' :
		print "ERROR: How many times to repeat?.\n"
		exp_type = "TYPE ERROR"
	elif p[1]['type']!='STRING' :
		print "ERROR: You can only repeat a string.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "STRING"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type,

## SAB KUCHH ACHCHHE SE DEKHO ISME
def p_expression_binary(p):
	'''expression 	: expression COMMA expression
					| expression ASSOCIATE_OP expression
					| expression RANGE_OP expression
					| expression SEARCH_MODIFY expression
					| expression SEARCH_MODIFY_NEG expression'''



#now we have finally got an expression for each term
	# # nonassoc    ++ --
	# #SPLIT
	# def p_term_01A(p):
	# 	''' term_01A : INCREMENT_OP term
	# 				| DECREMENT_OP term
	# 				| empty term_01A'''
	# 	global add
	# 	global term1ANUM
	# 	term1ANUM += 1
	# 	p[0] = "term_01A_" + str(term1ANUM)
	# 	add += "\nterm_01A_" + str(term1ANUM) +" -- { " + p[1]
	# 	term1ANUM +=1
	# 	add += p[2] + " };"

	# def p_term_01B(p):
	# 	''' term_01B : INCREMENT_OP term
	# 				| DECREMENT_OP term
	# 				| empty term'''
	# 	global add
	# 	global term1BNUM
	# 	term1BNUM +=1
	# 	p[0] = "term_01B_" +str(term1BNUM)
	# 	add += "\nterm_01B_" +str(term1BNUM) + " -- { " + "INC_DEC_OP_" + str(incdecopNUM) + p[2] + " };"

	# # right   **
	# def p_term_02(p):
	# 	''' term_02	: term_01A EXPONENT_OP term_02
	# 				| term_01A  empty empty
	# 				| term_01B EXPONENT_OP term_02
	# 				| term_01B  empty empty'''
	# 	global add
	# 	global term2NUM
	# 	global exponentopNUM
	# 	term2NUM +=1
	# 	exponentopNUM +=1
	# 	p[0] = "term_02_" + str(term2NUM)
	# 	add += "\nterm_02_" + str(term2NUM) + " -- { " + p[1] + p[2] + "_" + str(exponentopNUM) + p[3] + " };"
		
	# # right   ! ~ \ and unary + and -				# our expressions will not have "\" in them .. it is for the strings
	# def p_term_03(p):
	# 	''' term_03	: PLUS_OP term_02   %prec UPLUS
	# 				| MINUS_OP term_02  %prec UMINUS
	# 				| BIT_FLIP term_02
	# 				| NOT_OP term_02
	# 				| empty term_02'''
	# 	global add
	# 	p[0] = "term_03_" + str(term3NUM)
	# 	add += "term_03_" + str(term3NUM) + " -- { " + p[1] + "_" +str(plmibinoNUM)+ p[2] + " };"
	# # left    =~ !~
	# def p_term_04(p):
	# 	''' term_04	: term_04 SEARCH_MODIFY term_03
	# 				| term_04 SEARCH_MODIFY_NEG term_03
	# 				| term_03 empty empty'''
	# # left    * / % x
	# def p_term_05(p):
	# 	''' term_05	: term_05 MULTIPLICATION_OP term_04
	# 				| term_05 DIVISION_OP term_04
	# 				| term_05 MODULUS_OP term_04
	# 				| term_05 REP_OP term_04
	# 				| term_04 empty empty'''
	# #     left    + - .
	# def p_term_06(p):
	# 	''' term_06	: term_06 PLUS_OP term_05
	# 				| term_06 MINUS_OP term_05
	# 				| term_06 CONCATENATE term_05
	# 				| term_05 empty empty'''
	# #     left    << >>
	# def p_term_07(p):
	# 	''' term_07	: term_07 BIT_RIGHT_SHIFT term_06
	# 				| term_07 BIT_LEFT_SHIFT term_06
	# 				| term_06 empty empty'''
	# #     nonassoc    < > <= >= lt gt le ge
	# def p_term_08(p):
	# 	''' term_08	: term_07 GREATER_OP term_07
	# 				| term_07 LESS_OP term_07
	# 				| term_07 GREATER_EQUAL_OP term_07
	# 				| term_07 LESS_EQUAL_OP term_07
	# 				| term_07 empty empty'''
	# #     nonassoc    == != <=> eq ne cmp ~~ 		#not doing ~~
	# def p_term_09(p):
	# 	''' term_09	: term_08 EQUALS_OP term_08
	# 				| term_08 NOT_EQUALS_OP term_08
	# 				| term_08 COMPARE_OP term_08
	# 				| term_08 empty empty'''
	# #     left    &
	# def p_term_10(p):
	# 	''' term_10 : term_10 BIT_AND term_09
	# 				| term_09 empty empty'''
	# #     left    | ^
	# def p_term_11(p):
	# 	''' term_11	: term_11 BIT_OR term_10
	# 				| term_11 BIT_XOR term_10
	# 				| term_10 empty empty'''
	# #     left    &&
	# def p_term_12(p):
	# 	''' term_12	: term_12 AND_OP term_11
	# 				| term_11 empty empty'''
	# #     left    || //								# // not implemented:: defined(EXPR1) ? EXPR1 : EXPR
	# def p_term_13(p):
	# 	''' term_13	: term_13 OR_OP term_12
	# 				| term_12 empty empty'''
	# # nonassoc    ..  ... 							# not implemented ...
	# def p_term_14(p):
	# 	''' term_14 : term_13 RANGE_OP term_13
	# 				| term_13 empty empty'''
	# # right   = += -= *= etc. goto last next redo dump		##### see if we can implement goto, last, next, redo ... dump not implemented
	# def p_term_15(p):
	# 	''' term_15 : term_14 ADV_ASSIGNMENT_OP term_15
	# 				| term_14 ASSIGNMENT_OP term_15
	# 				| term_14 empty empty'''
	# # left    , =>
	# def p_term_16(p):
	# 	''' term_16	: term_16 COMMA term_15
	# 				| term_16 ASSOCIATE_OP term_15
	# 				| term_15 empty empty'''
	# # right   not
	# def p_term_17(p):
	# 	''' term_17 : term_16 NOT_STR_OP term_17
	# 				| term_16 empty empty'''
	# # left    and
	# def p_term_18(p):
	# 	''' term_18 : term_18 AND_STR_OP term_17
	# 				| term_17 empty empty'''
	# # left    or xor
	# def p_term_19(p):
	# 	''' term_19 : term_19 OR_STR_OP term_18
	# 				| term_19 XOR_STR_OP term_18
	# 				| term_18 empty empty'''

	# #########temporary
	# def p_expression_number(p):
	# 	'''expression : term_19
	# 	              | term'''



##################################################
#ERROR HANDLING
##################################################
def p_error(p):
	print "ERROR IN PARSING PHASE!!!"
	#panic mode recovery code



parser = yacc.yacc(debug=1)

def runparser(inputfile):
	program=open(inputfile).read()
	result=parser.parse(program,lexer=lexer, debug=1)
	print result
	print "\nSymbol Table :-\n"
	print symTable.symbolTable
	print "\nThree Address Code:-\n"
	print threeAddrCode.code

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)
