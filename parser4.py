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
    threeAddrCode.emit('','','EXIT','')
    symTable.deletescope('root')
    

def p_block(p):
    'block : BLOCK_BEGIN  statements  BLOCK_ENDS'

    p[0] = p[2]
    
def p_statments(p):
    'statements : statement statements'

    p[0]={}
    p[0]['beginlist']= threeAddrCode.merge(p[1].get('beginlist'),p[2].get('beginlist',[])) 
    p[0]['endlist']= threeAddrCode.merge(p[1].get('endlist'),p[2].get('endlist',[])) 

def p_statments_single(p):
	'statements : statement '

	p[0] = p[1]
	

def p_empty(p):
    'empty :'
    pass

# def p_empty_statements(p):
# 	'empty_statements : empty'

def p_statment(p):
    '''statement : assignment Marker 
    		     | declaration Marker
                 | returnStatement Marker
                 | functionCall Marker SEMICOLON
                 | whileStatement Marker
                 | forStatement Marker
                 | printStatement Marker
                 | functionStatement Marker
                 | lastStatement Marker
                 | nextStatement Marker
                 | ifthen Marker
                 | ifthenelse Marker
                 | useStatement Marker
                 | untillStatement Marker
                 | dowhileStatement Marker
                 | inputStatement Marker
                 | switchStatement Marker''' # implementinf ifthen and ifthenelse without nested loop

                 #    
                 # | loopcontrolStatement    
                 #      
                 #   
                 # 
                 # 
                 # | dowhileStatement
                 # | ternaryStatement 
                 # '''
    p[0] = {'type':"VOID",'beginlist' : p[1]['beginlist'] , 'endlist' : p[1]['endlist']}
    # p[0] = p[1]
    # print p[1]
    # print p[1].get('nextlist', [])
    nextList = p[1].get('nextlist', [])
    # print nextList
    threeAddrCode.backpatch(nextList, p[2]['quad'])



def p_useStatement(p):
	'useStatement : USE IDENTIFIER SEMICOLON'
	
def p_switchStatement(p):
	'switchStatement : SWITCH expression BLOCK_BEGIN caselist BLOCK_ENDS'
	


def p_caselist(p):
    '''caselist : CASE OPEN_PARANTHESIS expression CLOSE_PARANTHESIS block caselist
    			| ELSE  block 
                | empty '''
    

def p_inputStatement(p):
	'inputStatement : VARIABLE ASSIGNMENT_OP USER_INPUT_OP SEMICOLON'

	p[0]={'beginlist':[], 'nextlist':[],'endlist':[],'type':"VOID"}
	threeAddrCode.emit('','','INPUT','')




def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerif Marker block'

	if p[3]['type']!="BOOLEAN":
		print "line "+str(p.lineno(3))+" :Expression is not of boolean type"
		exp_type="TYPE ERROR"
	else:
		exp_type="VOID"

	threeAddrCode.backpatch(p[5]['truelist'],p[6]['quad'])
	p[0]={'type':exp_type,'nextlist': threeAddrCode.merge(p[5].get('falselist',[]),p[6].get('nextlist',[]))}
	p[0]['beginlist']=p[6].get('beginlist',[])
	p[0]['endlist']=p[6].get('endlist',[])


def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  Markerif Marker block ELSE Markerelse block'

	if p[3]['type']!="BOOLEAN":
		print "line "+str(p.lineno(3))+" :Expression is not of boolean type"
		exp_type="TYPE ERROR"
	else:
		exp_type="VOID"

	threeAddrCode.backpatch(p[5]['truelist'],p[6]['quad'])
	threeAddrCode.backpatch(p[5]['falselist'],p[9]['quad'])
	p[0]={'type':exp_type, 'nextlist' : [p[9]['quad']]}
	p[0]['beginlist']=threeAddrCode.merge( p[6].get('beginlist',[]), p[10].get('beginlist',[]))
	p[0]['endlist']=threeAddrCode.merge( p[6].get('endlist',[]), p[10].get('endlist',[]))

def p_Markerif(p):
	'Markerif : empty'
	p[0]={}
	p[0]['truelist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit(p[-2]['place'], '','TRUE_GOTO',-1)
	p[0]['falselist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit(p[-2]['place'], '','FALSE_GOTO',-1)

def p_Markerelse(p):
	'Markerelse : empty'
	p[0]={}
	# p[0]['nextlist']=[threeAddrCode.pointer_quad_next()]
	p[0]['quad']=threeAddrCode.pointer_quad_next()
	threeAddrCode.emit('', '','GOTO_END',-1)	

def p_lastStatement(p):
	'lastStatement : LAST SEMICOLON'
	p[0]={'beginlist':[], 'nextlist':[]}
	p[0]['endlist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit('','','GOTO',-1)

def p_nextStatement(p):
	'nextStatement : NEXT SEMICOLON'
	p[0]={'nextlist':[], 'endlist':[]}
	p[0]['beginlist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit('','','GOTO',-1)

def p_functionStament(p):
	'functionStatement : SUB IDENTIFIER Markerscope block'
	threeAddrCode.emit('','','JUMP_CALLING','')
	symTable.deletescope(p[2])
	p[0]={'beginlist':[], 'endlist':[]}

def p_Markerscope(p):
	'Markerscope : empty'
	p[0]={}
	p[0]['type']="FUNCTION"
	symTable.newvariableentry(p[-1],"FUNCTION",0)

	if  not symTable.proclist.has_key(p[-1]):
		symTable.enterproc(p[-1])
	else:
		symTable.removehash(p[-1])
		symTable.enterproc(p[-1])
	threeAddrCode.createCode(p[-1])
	threeAddrCode.emit('','',p[-1],'')
	

def p_functionCall(p):
	'functionCall : IDENTIFIER OPEN_PARANTHESIS  CLOSE_PARANTHESIS ' 

	p[0]={}

	if symTable.ifexist(p[1])==0:
		print "Function is not defined"
		p[0]['type']="TYPE ERROR"
	else:
		functiontype=symTable.getvalueofkey(p[1],'type')
		if functiontype=="FUNCTION":
			p[0]['type']=symTable.getvalueofkey(p[1],'returntype')
			threeAddrCode.emit('','','GOTO_LABEL',p[1])
		else:
			print "This is not a function"
		p[0]['place']=p[1]
		p[0]['beginlist']=[]
		p[0]['endlist']=[]

def p_printStatement(p):
	'printStatement : PRINT OPEN_PARANTHESIS expression CLOSE_PARANTHESIS SEMICOLON'

	# p[0] = {'place':symTable.newtmp()}
	p[0] = {}
	if p[3]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		exp_type = "VOID"
		threeAddrCode.emit(p[3]['type'], '', p[1], p[3]['place'])

	p[0]['type']=exp_type 
	p[0]['beginlist']=[]
	p[0]['endlist']=[]

def p_printStatement_no_paran(p):
	'printStatement : PRINT  expression  SEMICOLON'
	p[0]={}
	if p[2]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		exp_type = "VOID"
		threeAddrCode.emit(p[2]['type'], '', p[1], p[2]['place'])

	p[0]['type']=exp_type
	p[0]['beginlist']=[]
	p[0]['endlist']=[]					
	
def p_return(p):
    'returnStatement : RETURN expression SEMICOLON'

    p[0]={'type': p[2]['type'],'beginlist':[], 'endlist':[]}
    symTable.addintocurrentscope('returntype',p[2]['type'])
    threeAddrCode.emit(p[2]['place'],'',p[1],'')
    
def p_assignment(p):
    'assignment : VARIABLE ASSIGNMENT_OP expression SEMICOLON'

    if p[3]=="TYPE ERROR":
    	exp_type = "TYPE ERROR"
    else:
    	p[1]={'type':p[3]['type'], 'place':p[1]}
    	# add entry in the symbol table and fill in the type
    	symTable.newvariableentry(p[1]['place'], p[1]['type'], 0)
    	exp_type = "VOID"
    	threeAddrCode.emit(p[1]['place'], '',p[2], p[3]['place'])

    p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]} 

def p_assignment_specific_local(p):
	'assignment : LOCAL VARIABLE ASSIGNMENT_OP expression SEMICOLON'

	if p[4]=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		p[2]={'type':p[4]['type'], 'place':p[2]}
		# add entry in the symbol table and fill in the type
		symTable.newvariableentry(p[2]['place'], p[2]['type'], 0)
		exp_type = "VOID"
		threeAddrCode.emit(p[2]['place'], '',p[3], p[4]['place'])

	p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}

def p_assignment_specific(p):
    'assignment : PRIVATE VARIABLE ASSIGNMENT_OP expression SEMICOLON'

    if p[4]=="TYPE ERROR":
    	exp_type = "TYPE ERROR"
    else:
    	p[2]={'type':p[4]['type'], 'place':p[2]}
    	# add entry in the symbol table and fill in the type
    	symTable.newvariableentry(p[2]['place'], p[2]['type'], 1)
    	exp_type = "VOID"
    	threeAddrCode.emit(p[2]['place'], '',p[3], p[4]['place'])

    p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}

def p_assignment_adv(p):
	'assignment : VARIABLE ADV_ASSIGNMENT_OP expression SEMICOLON'

	exp_type = "VOID"
	if p[3]=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		varType = symTable.getvalueofkey_variable(p[1], 'type')
		if varType==None:
			print "Variable does not exist\n"
			exp_type_left = "TYPE ERROR"
		else:
			exp_type_left = varType
		p[1] = {'place':p[1], 'type':exp_type_left}
		# Dealing with the binary operation
		Adv_Op = p[2].split("=")[0]
		
		if Adv_Op=='x':
			if p[3]['type']!='NUMBER' :
				print "ERROR: How many times to repeat?.\n"
				exp_type="TYPE ERROR"
			elif p[1]['type']!='STRING' :
				print "ERROR: You can only repeat a string.\n"
				exp_type="TYPE ERROR"
		else:
			if p[1]['type']!='NUMBER' or p[3]['type']!='NUMBER' :
				print "ERROR: cannot perform operation\n"
				exp_type="TYPE ERROR"
	
	if exp_type=="VOID":
		threeAddrCode.emit(p[1]['place'], p[1]['place'], Adv_Op, p[3]['place'])
	else:
		print "Some error occured in advanced assignment\n"
	p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}



def p_while(p):
	'whileStatement : WHILE Marker OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerwhile  block'
	
	p[0]={'nextlist':[],'type' : 'VOID', 'beginlist':[], 'endlist':[]}

	

	if p[4]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[7]['beginlist'],p[2]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[7].get('endlist',[]),p[7].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[6].get('falselist',[]),p[0].get('nextlist',[]))
		threeAddrCode.emit('','','GOTO',p[2]['quad'])
	else:
		print "line "+str(p.lineno(4))+" :Expression is not of boolean type"

def p_Markerwhile(p):
	'Markerwhile : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-2]['place'],'','GOTO_MARK','-1')


def p_dowhileStatement(p):
	'dowhileStatement : DO block WHILE Marker OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerdowhile  SEMICOLON'

	p[0]={'nextlist':[],'type' : 'VOID', 'beginlist':[], 'endlist':[]}

	if p[6]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[2]['beginlist'],p[4]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[2].get('endlist',[]),p[2].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[8].get('falselist',[]),p[0].get('nextlist',[]))	
		threeAddrCode.emit('','','GOTO',p[4]['quad'])
	else:
		print "line "+str(p.lineno(6))+" :Expression is not of boolean type"

def p_markerdowhile(p):
	'Markerdowhile : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-2]['place'],'','GOTO_MARK','-1')




def p_untillStatement(p):
	'untillStatement : UNTIL Marker OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markeruntil  block'

	p[0]={'nextlist':[],'type' : 'VOID', 'beginlist':[], 'endlist':[]}
	

	if p[4]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[7]['beginlist'],p[2]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[7].get('endlist',[]),p[7].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[6].get('falselist',[]),p[0].get('nextlist',[]))
		threeAddrCode.emit('','','GOTO',p[2]['quad'])
	else:
		print "line "+str(p.lineno(4))+" :Expression is not of boolean type"

def p_Markeruntil(p):
	'Markeruntil : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-2]['place'],'','GOTO_MARK2','-1')


def p_for(p):
	'forStatement : FOR  OPEN_PARANTHESIS assignment   Marker  expression  SEMICOLON  Marker  VARIABLE ASSIGNMENT_OP expression CLOSE_PARANTHESIS  Markerfor  block'
	
	p[0]={}
	if p[5]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[13]['beginlist'],p[4]['quad'])
		#threeAddrCode.backpatch(p[13]['endlist'],p[7]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[13].get('endlist',[]),p[13].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[12].get('falselist',[]),p[0].get('nextlist',[]))	    	
	    # add entry in the symbol table and fill in the type
		
		p[8]={'type':p[10]['type'], 'place':p[8]}
		
		symTable.newvariableentry(p[8]['place'], p[8]['type'], 0)
		threeAddrCode.emit(p[8]['place'], '',p[9], p[10]['place'])
		threeAddrCode.emit('','','GOTO',p[4]['quad'])
	else:
		print "line "+str(p.lineno(5))+" :Expression is not of boolean type"
	p[0]['beginlist']=[]
	p[0]['endlist']=[]


def p_for_advass(p):
	'forStatement : FOR  OPEN_PARANTHESIS assignment   Marker  expression  SEMICOLON  Marker  VARIABLE ADV_ASSIGNMENT_OP expression CLOSE_PARANTHESIS  Markerfor  block'
	
	p[0]={}
	if p[5]['type']=="BOOLEAN":
		
		threeAddrCode.backpatch(p[13]['beginlist'],p[4]['quad'])
		threeAddrCode.backpatch(p[13]['endlist'],p[7]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[13].get('endlist',[]),p[13].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[12].get('falselist',[]),p[0].get('nextlist',[]))	    	
	    # add entry in the symbol table and fill in the type
		

		exp_type = "VOID"
		varType = symTable.getvalueofkey_variable(p[8], 'type')
		if varType==None:
			print  "line "+str(p.lineno(8))+" : Variable does not exist\n"
			exp_type_left = "TYPE ERROR"
		else:
			exp_type_left = varType
		p[8] = {'place':p[8], 'type':exp_type_left}
		# Dealing with the binary operation
		Adv_Op = p[9].split("=")[0]
		
		
		if p[8]['type']!='NUMBER' or p[10]['type']!='NUMBER' :
			print  "line "+str(p.lineno(9))+": cannot perform operation\n"
			exp_type="TYPE ERROR"
	
		if exp_type=="VOID":
			threeAddrCode.emit(p[8]['place'], p[8]['place'], Adv_Op, p[10]['place'])
		else:

			print  "line "+str(p.lineno(9))+" : Some error occured in advanced assignment\n"	
		threeAddrCode.emit('','','GOTO',p[4]['quad'])
	else:
		print "line "+str(p.lineno(5))+" :Expression is not of boolean type"
	p[0]['beginlist']=[]
	p[0]['endlist']=[]


def p_Markerfor2(p):
	'Markerfor2 : empty'


def p_Markerfor(p):
	'Markerfor : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-7]['place'],'','GOTO_MARK','-1')
	
def p_assignment_For_empty(p):
	'assignment : empty'


# def p_assignment_adv_specific(p):
#     '''assignment : PRIVATE VARIABLE ADV_ASSIGNMENT_OP expression SEMICOLON
#     				| LOCAL VARIABLE ADV_ASSIGNMENT_OP expression SEMICOLON'''	

# Earlier implementation remanants
	# def p_lefthandside(p):
	# 	'''lefthandside : PRIVATE type decList 
	# 					| PRIVATE OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
		
	# def p_lefthandsided(p):
	# 	'''lefthandside : LOCAL  type decList 
	# 					| LOCAL OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
		
	# def p_lefthandsideb(p):
	# 	'''lefthandside : OPEN_PARANTHESIS type decList CLOSE_PARANTHESIS'''
		

	# def p_lefthandsidec(p):
	# 	'lefthandside : type'
	# def p_declaration(p):
	# 	'declaration :  lefthandside SEMICOLON'

def p_declaration(p):
	'declaration :  VARIABLE decList SEMICOLON'
	varList = [p[1]] + p[2]
	for varName in varList:
		symTable.newvariableentry(varName, '', 0)
		threeAddrCode.emit('', '', 'DECLARATION', varName)
	p[0]={'type':"VOID", 'beginlist':[], 'endlist':[]}

def p_declaration_specific_private(p):
	'declaration :  PRIVATE VARIABLE decList SEMICOLON'
	varList = [p[2]] + p[3]
	# print varList
	for varName in varList:
		symTable.newvariableentry(varName, '', 1)
		threeAddrCode.emit('', '', 'DECLARATION', varName)
	p[0]={'type':"VOID", 'beginlist':[], 'endlist':[]}

def p_declaration_specific(p):
	'declaration :  LOCAL VARIABLE decList SEMICOLON'
	varList = [p[2]] + p[3]
	for varName in varList:
		symTable.newvariableentry(varName, '', 0)
		threeAddrCode.emit('', '', 'DECLARATION', varName)
	p[0]={'type':"VOID", 'beginlist':[], 'endlist':[]}
	
# def p_decList(p):
# 	'''decList :  COMMA type decList
# 	           |  empty'''
	
def p_decList(p):
	'decList :  COMMA VARIABLE decList'
	p[0]=[p[2]]+p[3]

def p_decList_empty(p):
	'decList :  empty'
	p[0]=[]



def p_termfunction(p):
	'term : functionCall'
	p[0]=p[1]	
	

# def p_parameters(p):
# 	'''parameters 	: expression COMMA parameters
# 					| expression 
# 					| empty '''
					#### KAISE START KARU. SPLIT KARNA PADEGA
	





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

	p[0] = {'type':'STRING', 'value':p[1]}

def p_res_string(p):
	'string : RES_STRING'

	p[0] = {'type':'RES_STRING', 'value':p[1]}
	
def p_number(p):
	''' number  : NUMBER
				| SCI_NOT
				| FLOAT
				| HEXADECIMAL
				| OCTAL'''

	p[0] = {'type':'NUMBER', 'value':p[1]}

#SPLIT
# def p_variable(p):
# 	''' variable 	: VARIABLE
# 					| VARIABLE OPEN_BRACKET NUMBER CLOSE_BRACKET'''  ### Ye Bracket hai ya parenthesis???

# def p_variable(p):
# 	'variable : VARIABLE'
	
# 	p[0] = {'place':p[1]}

def p_term(p):
	''' term 	:  number 
				|  string  '''

	p[0] = p[1]
	p[0]['place'] = symTable.newtmp()
	threeAddrCode.emit(p[0]['place'], '', '=', p[1]['value'])

def p_term_var(p):
	'term : VARIABLE'

	varType = symTable.getvalueofkey_variable(p[1], 'type')
	if varType==None:
		print "Variable does not exist\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = varType

	p[0] = {'place':p[1], 'type':exp_type}

def p_term_exp(p):
	'term : OPEN_PARANTHESIS expression CLOSE_PARANTHESIS'

	p[0] = p[2]

# def p_type_var(p):
# 	'type : variable'

# 	p[0] = p[1]

####
# def p_type(p):
# 	' type : ARRAY'

def p_expression_unary(p):								#INCREMENT_OP and DECREMENT_OP deleted
	''' expression : PLUS_OP expression   %prec UPLUS
				   | MINUS_OP expression  %prec UMINUS
				   | BIT_FLIP expression'''

	p[0] = {'place':symTable.newtmp()}

	if p[2]['type']!='NUMBER' :
		print "line "+str(p.lineno(2))+" : Type error.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "NUMBER"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type']= exp_type
	# p[0]['value']=str(p[1])+str(p[2]['value'])

def p_expression_unary_notOp(p):
	'expression : NOT_OP expression'
	
	p[0] = {'place':symTable.newtmp(), 'truelist':p[2]['falselist'], 'falselist':p[2]['truelist']}
	if p[2]['type']!='BOOLEAN' :
		print "line "+str(p.lineno(2))+" : Type error in expression.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']= str(p[1])+str(p[2]['value'])

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
		print "line "+str(p.lineno(2))+" : Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['truelist'], p[3]['quad'])
	p[0]['type']=exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[4]['value'])

def p_exp_or_op(p):
	'expression : expression OR_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'truelist':threeAddrCode.merge(p[1]['truelist'], p[4]['truelist']), 'falselist':p[4]['falselist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "line "+str(p.lineno(2))+" : Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['falselist'], p[3]['quad'])
	p[0]['type']=exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[4]['value'])

def p_expression_binary_relational(p):
	'''expression : expression EQUALS_OP expression
				  | expression NOT_EQUALS_OP expression
				  | expression GREATER_OP expression
				  | expression LESS_OP expression
				  | expression GREATER_EQUAL_OP expression
				  | expression LESS_EQUAL_OP expression'''

	if p[1]['type']!='NUMBER' or p[3]['type']!='NUMBER' :
		print "line "+str(p.lineno(2))+" : cannot compare\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"

	p[0] = {'type' : exp_type, 'place':symTable.newtmp(), 'truelist':[threeAddrCode.pointer_quad_next()], 'falselist':[1+threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[3]['value'])

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
		print "line "+str(p.lineno(2))+" : cannot perform operation\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "NUMBER"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[3]['value'])

def p_expression_concat(p):
	'expression : expression CONCATENATE expression'

	p[0] = {'place':symTable.newtmp()}
	# if p[1]['type']!='STRING' or p[3]['type']!='STRING' :
	# 	print "ERROR: Concatenation operation works only on strings\n"
	# 	exp_type = "TYPE ERROR"
	# else:
	exp_type = 'STRING'
	threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[3]['value'])

def p_expression_repeatition(p):
	'expression : expression REP_OP expression'

 	p[0] = {'place':symTable.newtmp()}
	if p[3]['type']!='NUMBER' :
		print "line "+str(p.lineno(2))+" : How many times to repeat?.\n"
		exp_type = "TYPE ERROR"
	elif p[1]['type']!='STRING' :
		print "line "+str(p.lineno(2))+" : You can only repeat a string.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "STRING"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[3]['value'])

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
	# print result
	# print "\nSymbol Table :-\n"
	# print symTable.symbolTable
	print "\nThree Address Code:-\n"
	# print threeAddrCode.code
	for scopes in threeAddrCode.code:
		count = 0
		print "In the scope "+str(scopes)+" :-"
		for TAC in threeAddrCode.code[scopes]:
			print "\t"+str(count)+"\t"+str(TAC)
			count+=1

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)
