import yacc
import symbolTable
import tac

import re

import sys
import os

from lexer import tokens,lexer


# def p_start(p):
#     '''start : block
#              | statements'''




# def p_block(p):
# 	'block :BLOCK_BEGIN statements BLOCK_ENDS'

symTable = symbolTable.SymbolTable()
threeAddrCode = tac.Tac(symTable)
switch_hash={}
temp_line=0
code_string=".section .text\n"
code_string+="true:\nmovl\t$1,%eax\nret\n"
code_string+=".globl _start"
code_string+="\n"
code_string+="_start:\n"
data_string=".section .data\n"
data_strings={}
cod_strings={}
temp_add={}
global_vars={}
function_list={}
function_list[0]=['root1']
function_list_linear={'root1':"VOID"}
global_strings={}
print_flag=0
backPatchingStrings={}

###############Print Number##############################################

printIntCode = "\n\n\njmp EndPrintNum\n\
printIntNumber:\n\
	pushl %eax #save the  registers\n\
	pushl %ebx\n\
	pushl %ecx\n\
	pushl %edx\n\
	pushl %edi\n\
	pushl %esi\n\
	pushl %ebp\n\
	\n\
    movl %ecx, %eax #storing number in %eax to divide it by 10 and extract digits one by one\n\
    movl %esp, %esi   #storing the initial position of the stack pointer in %esi register\n\
    labl:\n\
    #%eax has quotient after div and %edx has the remainder after division. div R1 does %eax / R1\n\
    cdq    # preparing to divide\n\
    movl $10, %ebx    # store 10 in %ebx register which is the divisor             \n\
    idivl %ebx   #divide number by 10.remainder and quotient are stored in %edx and %eax resp. \n\
                 #Remainder is the least significant digit of the current number \n\
    pushl %edx   # pushing the least significant digit (remainder) into stack\n\
    cmpl $0, %eax #comparing quotient with 0 to ascertain whether have we extracted all digits\n\
    jne labl #If q not equal to zero,then we still need to continue extracting more digits,so\n\
             # jump back to labl  \n\
    jmp print_num   # if q=0, then jump to print_num\n\
    \n\
 print_num:\n\
    popl %edx  # poping the topmost element from stack which would be the highest significant \n\
               # digit of our number as it was pushed last into the stack\n\
    addl $48, %edx  # converting the digit to ascii character by adding 48 to that digit \n\
                   # as, 48 is the ascii code for digit 0, 49 for 1, 50 for 2 and so on...\n\
    pushl %edx # s is randomly chosen memory location to store it\n\
                      # we store it in a memory location to print it by using sytem call no.4 \n\
    \n\
    movl $4, %eax  # 4 is sys call number\n\
    movl $1, %ebx  # 1 refers to stdout\n\
    movl %esp, %ecx  # number+50 refers to location where the digit is stored in memory \n\
    movl $1, %edx    # size of buffer =1, as we print one digit at a time \n\
    int $0x80\n\
    popl %edx       # Pop the digit on the top  \n\
    cmp %esp, %esi   # checking if the current stack pointer has reached the initial postion\n\
                     # of stack pointer which we stored in %esi at the beginning, before \n\
                     # starting to push any value\n\
    jne print_num   #if stack pointer has not reached the initial position of stack, we jump \n\
                    #back to print_num label to pop more values and print them.\n\
    popl %ebp #restore the registers\n\
    popl %esi\n\
    popl %edi\n\
    popl %edx\n\
    popl %ecx\n\
    popl %ebx\n\
    popl %eax\n\
    ret  \n\
    EndPrintNum:\n"



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
    '''statement : assignment Marker SEMICOLON
    		     | declaration Marker
    		     | array_assignment Marker
                 | returnStatement Marker
                 | functionCall Marker SEMICOLON
                 | whileStatement Marker
                 | forStatement Marker
                 | printStatement Marker
                 | functionStatement Marker
                 | lastStatement Marker
                 | nextStatement Marker
                 | ifthen Marker
                 | unless Marker
                 | ifthenelse Marker
                 | useStatement Marker
                 | untillStatement Marker
                 | dowhileStatement Marker
                 | inputStatement Marker
                 | switchStatement Marker
                 | ternaryStatement Marker SEMICOLON'''

                 #    
                 # | loopcontrolStatement    
                 #      
                 #   
                 # 
                 # 
                 # | dowhileStatement 
                 # '''
    p[0] = {'type':"VOID",'beginlist' : p[1]['beginlist'] , 'endlist' : p[1]['endlist']}
    # p[0] = p[1]
    # print p[1]
    # print p[1].get('nextlist', [])
    nextList = p[1].get('nextlist', [])
    # print nextList
    threeAddrCode.backpatch(nextList, p[2]['quad'])

def p_ternaryStatement(p):
	'''ternaryStatement : expression QUESTION_MARK Marker_true Marker expression COLON Marker_false expression 
					 | expression QUESTION_MARK Marker_true Marker assignment COLON Marker_false assignment '''

	if p[1]['type']!="BOOLEAN":
		print "ERROR: line "+str(p.lineno(1))+" : Expression in ternary statement is not boolean\n"
	else:
		if p[5]['type']==p[8]['type']:
			threeAddrCode.backpatch(p[3]['truelist'],p[4]['quad'])
			threeAddrCode.backpatch(p[3]['falselist'],p[7]['quad'])
			p[0]={'type':p[5]['type'], 'nextlist' : p[7]['nextlist']}
		else:
			print "ERROR: line "+str(p.lineno(5))+" : The types of the expressions in ternary expression must be same..\n"

	p[0]['beginlist']=[]
	p[0]['endlist']=[]
	# print "as"+str(p[0]['nextlist'])

def p_Marker_true(p):
	'Marker_true : empty'
	p[0]={}
	p[0]['truelist']=[threeAddrCode.pointer_quad_next()]
	#threeAddrCode.emit(p[-2]['place'], '','TRUE_GOTO',-1)
	p[0]['falselist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit(p[-2]['place'], '','FALSE_GOTO',-1)

def p_Marker_false(p):
	'Marker_false : empty'
	p[0]={}
	p[0]['nextlist']=[threeAddrCode.pointer_quad_next()]
	
	threeAddrCode.emit('', '','GOTO_END',-1)	
	p[0]['quad']=threeAddrCode.pointer_quad_next()

def p_useStatement(p):
	'''useStatement : USE IDENTIFIER SEMICOLON
					| USE VERSION SEMICOLON'''

	p[0] = symTable.newvariableentry(p[2], 'MODULE_OR_VERSION', 0)
	p[0] = {'type':"VOID", 'beginlist':[], 'endlist':[]}

def p_useStatement_list(p):
	'useStatement : USE IDENTIFIER module_list SEMICOLON'


# Not implemented yet.... to be done after implementation of parameters
def p_module_list(p):
	'module_list : empty'
	
def p_switchStatement_paran(p):
	'switchStatement : SWITCH expression BLOCK_BEGIN Marker_switch CASE OPEN_PARANTHESIS expression Marker_caselist CLOSE_PARANTHESIS block Marker_quit caselist BLOCK_ENDS'

	check = symTable.getvalueofkey_variable('Switch', 'type')
	if check==None:
		print "ERROR: line "+str(p.lineno(1))+" :'Switch' module not included\nYou might want to include command \"use Switch\" "
		exp_type = "TYPE ERROR"
	else:
		exp_type="VOID"
		threeAddrCode.backpatch(p[8]['falselist'], p[11]['quad'])
		# print "qwertyu "+str(p[3]['quad'])
	p[0]={'beginlist':[], 'endlist':[]}

	p[0]['nextlist']= threeAddrCode.merge(p[11]['nextlist'], p[12]['nextlist'])
	# print "\n hooooooasdo "
	# print p[0]['nextlist']

# def p_switchStatement(p):
# 	'switchStatement : SWITCH expression BLOCK_BEGIN Marker_switch CASE expression Marker_caselist block Marker_quit caselist BLOCK_ENDS'

# 	check = symTable.getvalueofkey_variable('Switch', 'type')
# 	if check==None:
# 		print "ERROR: line "+str(p.lineno(3))+" :'Switch' module not included\nYou might want to include command \"use Switch\" "
# 		exp_type = "TYPE ERROR"
# 	else:
# 		exp_type="VOID"

# 		threeAddrCode.backpatch(p[7]['falselist'], p[9]['quad'])
# 		# print "qwertyu "+str(p[3]['quad'])


# 	p[0]={'type':exp_type, 'beginlist':[], 'endlist':[], 'nextlist':p[9]['nextlist']}

def p_Marker_switch(p):
	'Marker_switch : empty'

	global switch_hash 
	switch_hash = {'LHS':p[-2]['place'], 'type':p[-2]['type']}
	p[0] = {'quad':threeAddrCode.pointer_quad_next()}
	# p[0] = {'LHS':p[-2]['place'], 'type':p[-2]['type']}
	# label = threeAddrCode.newLabel();
	# threeAddrCode.emit('', p[-1]['place'], 'GOTO_SWITCH', label)
	# p[0]['label'] = label

def p_caselist_paran(p):
    'caselist :  CASE OPEN_PARANTHESIS expression Marker_caselist CLOSE_PARANTHESIS block Marker_quit caselist'

    p[0]={}
    threeAddrCode.backpatch(p[4]['falselist'], p[7]['quad'])
    if p[4]['type']=="TYPE ERROR":
    	print "ERROR: line "+str(p.lineno(1))+" : cannot compare\n"

    
    # p[0]={'nextlist':[]}
    p[0]['nextlist']= threeAddrCode.merge(p[7]['nextlist'], p[8]['nextlist'])
    # print "\n hooooooooooo "
    # print p[0]['nextlist']

# def p_caselist(p):
#     'caselist : CASE expression Marker_caselist block caselist'

    # if p[2]['type']!='NUMBER' or p[-1]['type']!='NUMBER' :
    # 	print "ERROR: line "+str(p.lineno(2))+" : cannot compare\n"
    # else:
    # 	threeAddrCode.emit(symTable.newtmp(), p[2]['place'], '==', p[-1]['LHS'])

    # p[0] = {'type' : exp_type, 'place':symTable.newtmp(), 'truelist':[threeAddrCode.pointer_quad_next()], 'falselist':[1+threeAddrCode.pointer_quad_next()]}
    # threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place']



def p_caselist_else(p):
    'caselist : ELSE block Marker_quit'

    p[0]={'nextlist':p[3]['nextlist']}
    # p[0]={'nextlist':[]}
    # p[0]={'nextlist':[threeAddrCode.pointer_quad_next()]}
    # threeAddrCode.backpatch(p[3]['falselist'], p[3]['quad'])
   	# threeAddrCode.backpatch([p[-2]['quad']], )

def p_caselist_empty(p):
	'caselist : empty'

	p[0]={'nextlist':[]}
	# p[0]={'nextlist':[threeAddrCode.pointer_quad_next()]}
    
def p_Marker_caselist(p):
	'Marker_caselist : empty'

	global switch_hash
	p[0]={'type':"VOID"}
	if p[-1]['type']!='NUMBER' or switch_hash['type']!='NUMBER' :
		# print "ERROR: line "+str(temp_line)+" : cannot compare\n"
		p[0]['type']="TYPE ERROR"
	else:
		threeAddrCode.emit(symTable.newtmp(), p[-1]['place'], '==', switch_hash['LHS'])
	p[0]['falselist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit('', '', 'GOTO_SWITCH', '-1')

def p_marker_quit(p):
	'Marker_quit : empty'

	p[0] = {'nextlist':[threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit('', '', 'GOTO_SWITCH', '-1')
	p[0]['quad']= threeAddrCode.pointer_quad_next()

def p_inputStatement(p):
	'inputStatement : VARIABLE ASSIGNMENT_OP USER_INPUT_OP SEMICOLON'

	p[0]={'beginlist':[], 'nextlist':[],'endlist':[],'type':"VOID"}
	threeAddrCode.emit('','','INPUT','')


def p_unless(p):
	'unless : UNLESS OPEN_PARANTHESIS expression CLOSE_PARANTHESIS MarkerUnless Marker block'

	if p[3]['type']!="BOOLEAN":
		print "ERROR: line "+str(p.lineno(3))+" :Expression is not of boolean type"
		exp_type="TYPE ERROR"
	else:
		exp_type="VOID"

	threeAddrCode.backpatch(p[5]['truelist'],p[6]['quad'])
	p[0]={'type':exp_type,'nextlist': threeAddrCode.merge(p[5].get('falselist',[]),p[6].get('nextlist',[]))}
	p[0]['beginlist']=p[7].get('beginlist',[])
	p[0]['endlist']=p[7].get('endlist',[])

def p_MarkerUnless(p):
	'MarkerUnless : empty'
	p[0]={}
	p[0]['truelist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit(p[-2]['place'], '','FALSE_GOTO',-1)
	p[0]['falselist']=[threeAddrCode.pointer_quad_next()]
	#threeAddrCode.emit(p[-2]['place'], '','TRUE_GOTO',-1)
	# print "hsjb"+str(p[0]['truelist'])
	# print "hsjbf"+str(p[0]['falselist'])

def p_ifthen(p):
	'ifthen : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerif Marker block'

	if p[3]['type']!="BOOLEAN":
		print "ERROR: line "+str(p.lineno(3))+" :Expression is not of boolean type"
		exp_type="TYPE ERROR"
	else:
		exp_type="VOID"

	threeAddrCode.backpatch(p[5]['truelist'],p[6]['quad'])
	p[0]={'type':exp_type,'nextlist': threeAddrCode.merge(p[5].get('falselist',[]),p[6].get('nextlist',[]))}
	p[0]['beginlist']=p[7].get('beginlist',[])
	p[0]['endlist']=p[7].get('endlist',[])


def p_ifthenelse(p):
	'ifthenelse : IF OPEN_PARANTHESIS expression CLOSE_PARANTHESIS  Markerif Marker block ELSE Markerelse block '

	if p[3]['type']!="BOOLEAN":
		print "ERROR: line "+str(p.lineno(3))+" :Expression is not of boolean type"
		exp_type="TYPE ERROR"
	else:
		exp_type="VOID"

	threeAddrCode.backpatch(p[5]['truelist'],p[6]['quad'])
	threeAddrCode.backpatch(p[5]['falselist'],p[9]['quad'])
	p[0]={'type':exp_type, 'nextlist' : p[9]['nextlist']}
	p[0]['beginlist']=threeAddrCode.merge( p[7].get('beginlist',[]), p[10].get('beginlist',[]))
	p[0]['endlist']=threeAddrCode.merge( p[7].get('endlist',[]), p[10].get('endlist',[]))

def p_Markerif(p):
	'Markerif : empty'
	p[0]={}
	p[0]['truelist']=[threeAddrCode.pointer_quad_next()]
	#threeAddrCode.emit(p[-2]['place'], '','TRUE_GOTO',-1)
	p[0]['falselist']=[threeAddrCode.pointer_quad_next()]
	threeAddrCode.emit(p[-2]['place'], '','FALSE_GOTO',-1)
	# print "hsjb"+str(p[0]['truelist'])
	# print "hsjbf"+str(p[0]['falselist'])

def p_Markerelse(p):
	'Markerelse : empty'
	p[0]={}
	p[0]['nextlist']=[threeAddrCode.pointer_quad_next()]
	
	threeAddrCode.emit('', '','GOTO_END',-1)	
	p[0]['quad']=threeAddrCode.pointer_quad_next()

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
	global function_list_linear
	global function_list
	function_list_linear[p[2]]="VOID"
	if  symTable.symbolTable['root'][p[2]]['scope_depth'] in function_list:
		function_list[symTable.symbolTable['root'][p[2]]['scope_depth']].append(p[2])
	else :
		function_list[symTable.symbolTable['root'][p[2]]['scope_depth']]=[p[2]]
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
	threeAddrCode.emit('','','FUNC_LABEL',p[-1])
	

def p_functionCall(p):
	'functionCall : IDENTIFIER OPEN_PARANTHESIS  CLOSE_PARANTHESIS ' 

	p[0]={}

	if symTable.ifexist(p[1])==0:
		print "ERROR: line "+str(p.lineno(1))+" : Function is not defined"
		p[0]['type']="TYPE ERROR"
	else:
		functiontype=symTable.getvalueofkey(p[1],'type')
		if functiontype=="FUNCTION":
			p[0]['type']=symTable.getvalueofkey(p[1],'returntype')
			threeAddrCode.emit('','','GOTO_LABEL',p[1])
		else:
			print "ERROR: line "+str(p.lineno(1))+" :This is not a function"
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
    if p[2]['type']!="UNDEFINED":
    	symTable.addintocurrentscope('returntype',p[2]['type'])
    else:
    	print "ERROR: You have returned a function from a function indirectly\n\tMake sure that it does not form infinite loop\n"
    	print "\n\tHINT:: If there is no infinite loop, try placing the assignment \n\t\tstatement of returned variable with numerical or string value\n\t\t closer to the return statement than the assignment of \n\t\tthe returned variable to a function\n"
    threeAddrCode.emit(p[2]['place'],'',p[1],'')
    global global_strings 
    # if p[2].has_key('value'):
    # 	global_strings[p[2]['place']]=
    
def p_assignment(p):
    'assignment : VARIABLE ASSIGNMENT_OP expression '

    if p[3]['type']=="TYPE ERROR":
    	exp_type = "TYPE ERROR"
    else:
    	p[1]={'type':p[3]['type'], 'place':p[1]}
    	# add entry in the symbol table and fill in the type
    	symTable.newvariableentry(p[1]['place'], p[1]['type'], 0)
    	exp_type = "VOID"
    	threeAddrCode.emit(p[1]['place'], '',p[2], p[3]['place'])

    p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}
    
    global global_strings 
    if p[3].has_key('value'):
    	p[1]['value']=p[3]['value']
    	global_strings[p[1]['place']]=p[3]['value']
    	print "KOKOKOKOKOKOKOKOKOKOKOKKKKKKKOKO"
    	print global_strings


def p_assignment_to_array_elements(p):
    'assignment : ARRAY OPEN_BRACKET NUMBER CLOSE_BRACKET ASSIGNMENT_OP expression '

    if p[3]['type']=="TYPE ERROR":
    	exp_type = "TYPE ERROR"
    else:
    	p[1]={'type':p[3]['type'], 'place':p[1]}
    	# add entry in the symbol table and fill in the type
    	symTable.newvariableentry(p[1]['place'], p[1]['type'], 0)
    	exp_type = "VOID"
    	threeAddrCode.emit(p[1]['place'], '',p[2], p[3]['place'])

    p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]} 

def p_assignment_specific_local(p):
	'assignment : LOCAL VARIABLE ASSIGNMENT_OP expression '

	if p[4]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		p[2]={'type':p[4]['type'], 'place':p[2]}
		# add entry in the symbol table and fill in the type
		symTable.newvariableentry(p[2]['place'], p[2]['type'], 0)
		exp_type = "VOID"
		threeAddrCode.emit(p[2]['place'], '',p[3], p[4]['place'])

	p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}
	p[1]={}

def p_assignment_specific(p):
    'assignment : PRIVATE VARIABLE ASSIGNMENT_OP expression '

    if p[4]['type']=="TYPE ERROR":
    	exp_type = "TYPE ERROR"
    else:
    	p[2]={'type':p[4]['type'], 'place':p[2]}
    	# add entry in the symbol table and fill in the type
    	symTable.newvariableentry(p[2]['place'], p[2]['type'], 1)
    	exp_type = "VOID"
    	threeAddrCode.emit(p[2]['place'], '',p[3], p[4]['place'])

    p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}
    p[1]={}

def p_assignment_adv(p):
	'assignment : VARIABLE ADV_ASSIGNMENT_OP expression '

	exp_type = "VOID"
	if p[3]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		varType = symTable.getvalueofkey_variable(p[1], 'type')
		if varType==None:
			print "ERROR: Variable does not exist\n"
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
		print "Error: Some error occured in advanced assignment\n"
	p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}



def p_while(p):
	'whileStatement : WHILE Marker OPEN_PARANTHESIS expression CLOSE_PARANTHESIS Markerwhile  block'
	
	p[0]={'nextlist':[],'type' : 'VOID', 'beginlist':p[7]['beginlist'], 'endlist':p[7]['endlist']}

	

	if p[4]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[7]['beginlist'],p[2]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[7].get('endlist',[]),p[7].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[6].get('falselist',[]),p[0].get('nextlist',[]))
		threeAddrCode.emit('','','GOTO',p[2]['quad'])
	else:
		print "ERROR: line "+str(p.lineno(4))+" :Expression is not of boolean type"

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
		print "ERROR: line "+str(p.lineno(6))+" :Expression is not of boolean type"

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
		print "ERROR: line "+str(p.lineno(4))+" :Expression is not of boolean type"

def p_Markeruntil(p):
	'Markeruntil : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-2]['place'],'','GOTO_MARK2','-1')


def p_for(p):
	'forStatement : FOR  OPEN_PARANTHESIS assignment SEMICOLON  Marker  expression  SEMICOLON  Marker  VARIABLE ASSIGNMENT_OP expression CLOSE_PARANTHESIS  Markerfor  block'
	
	p[0]={}
	if p[6]['type']=="BOOLEAN":
		threeAddrCode.backpatch(p[14]['beginlist'],p[5]['quad'])
		#threeAddrCode.backpatch(p[13]['endlist'],p[7]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[14].get('endlist',[]),p[14].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[13].get('falselist',[]),p[0].get('nextlist',[]))	    	
	    # add entry in the symbol table and fill in the type
		
		p[9]={'type':p[11]['type'], 'place':p[9]}
		
		symTable.newvariableentry(p[9]['place'], p[9]['type'], 0)
		threeAddrCode.emit(p[9]['place'], '',p[10], p[11]['place'])
		threeAddrCode.emit('','','GOTO',p[5]['quad'])
	else:
		print "ERROR: line "+str(p.lineno(6))+" :Expression is not of boolean type"
	p[0]['beginlist']=[]
	p[0]['endlist']=[]


def p_for_advass(p):
	'forStatement : FOR  OPEN_PARANTHESIS assignment  SEMICOLON  Marker  expression  SEMICOLON  Marker  VARIABLE ADV_ASSIGNMENT_OP expression CLOSE_PARANTHESIS  Markerfor  block'
	
	p[0]={}
	if p[6]['type']=="BOOLEAN":
		
		threeAddrCode.backpatch(p[14]['beginlist'],p[5]['quad'])
		threeAddrCode.backpatch(p[14]['endlist'],p[8]['quad'])
		p[0]['nextlist']=threeAddrCode.merge(p[14].get('endlist',[]),p[14].get('nextlist',[]))
		p[0]['nextlist']=threeAddrCode.merge(p[13].get('falselist',[]),p[0].get('nextlist',[]))	    	
	    # add entry in the symbol table and fill in the type
		

		exp_type = "VOID"
		varType = symTable.getvalueofkey_variable(p[9], 'type')
		if varType==None:
			print  "ERROR: line "+str(p.lineno(9))+" : Variable does not exist\n"
			exp_type_left = "TYPE ERROR"
		else:
			exp_type_left = varType
		p[9] = {'place':p[9], 'type':exp_type_left}
		# Dealing with the binary operation
		Adv_Op = p[10].split("=")[0]
		
		
		if p[9]['type']!='NUMBER' or p[11]['type']!='NUMBER' :
			print  "ERROR: line "+str(p.lineno(10))+": cannot perform operation\n"
			exp_type="TYPE ERROR"
	
		if exp_type=="VOID":
			threeAddrCode.emit(p[9]['place'], p[9]['place'], Adv_Op, p[11]['place'])
		else:

			print  "ERROR: line "+str(p.lineno(10))+" : Some error occured in advanced assignment\n"	
		threeAddrCode.emit('','','GOTO',p[5]['quad'])
	else:
		print "ERROR: line "+str(p.lineno(6))+" :Expression is not of boolean type"
	p[0]['beginlist']=[]
	p[0]['endlist']=[]


def p_Markerfor(p):
	'Markerfor : empty'
	p[0]={'falselist' : [threeAddrCode.pointer_quad_next()]}
	threeAddrCode.emit(p[-7]['place'],'','GOTO_MARK','-1')
	
def p_assignment_For_empty(p):
	'assignment : empty'

	p[0]={'beginlist':[], 'endlist':[]}


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

	p[0] = p[1]
	new_name = p[1]['place']
	# print p[1]['place']
	p[0]['place'] = symTable.newtmp()
	threeAddrCode.emit(p[0]['place'], '', '=', new_name)
	

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

	# print p[1]
	# print "BBBBBBBBBBBBBBBBBBBBBBBBBB"
	# print re.sub(r'\\', '\\\\', p[1])
	# string_value = re.sub(r'\\', '\\\\', p[1])
	# print string_value
	# print "AAAAAAAAAAAAAAAAAAAAAAAAA"
	# p[0] = {'type':'STRING', 'value':string_value}
	temp=re.match(r'\'(.*)\'',p[1]).group(1)
	p[0] = {'type':'STRING', 'value':p[1]}

def p_res_string(p):
	'string : RES_STRING'

	temp=re.match(r'\"(.*)\"',p[1]).group(1)
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
	global global_strings
	global_strings[p[0]['place']]=p[1]['value']
	print global_strings
	print "NNIIINNNNNNNNNNNNNNNNNIIIIIIIIIIIIIIIIIII"

def p_term_var(p):
	'term : VARIABLE'

	varType = symTable.getvalueofkey_variable(p[1], 'type')
	if varType==None:
		print "ERROR: line "+str(p.lineno(1))+" :Variable"+p[1]+" does not exist\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = varType

	p[0] = {'place':p[1], 'type':exp_type}
	p[0]['place'] = symTable.newtmp()
	threeAddrCode.emit(p[0]['place'], '', '=', p[1])
	print p[1]
	print "qawwsxedefmngvjnnnnnnnnnnnnnnnnnnnntjm"
	global global_strings
	if global_strings.has_key(p[1]):
		global_strings[p[0]['place']]=global_strings[p[1]]
		print "QWERTYUIOPASDFGHJKZXCVBNM<"
		print global_strings


def p_term_exp(p):
	'term : OPEN_PARANTHESIS expression CLOSE_PARANTHESIS'

	p[0] = p[2]

def p_term_arr_element(p):
	'term : ARRAY OPEN_BRACKET NUMBER CLOSE_BRACKET'

	varType = symTable.getvalueofkey_array(p[1],p[3],'type')
	if varType==None:
		print "ERROR: line "+str(p.lineno(1))+" :Array "+p[1]+" element does not exist\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = varType

	p[0] = {'place':p[1], 'type':exp_type}

def p_array_assignment(p):
	' array_assignment : ARRAY ASSIGNMENT_OP OPEN_PARANTHESIS expression arrayList CLOSE_PARANTHESIS SEMICOLON'

	if p[4]['type']=="TYPE ERROR" or p[5]['type']=="TYPE ERROR":
		exp_type = "TYPE ERROR"
	else:
		p[5]['elements'].insert(0, {'type':p[4]['type']})
		p[1]={'place':p[1], 'elements':p[5]['elements']}
		# add entry in the symbol table and fill in the type
		symTable.newarrayentry(p[1]['place'], p[1]['elements'],0)
		exp_type = "VOID"
		threeAddrCode.emit(p[1]['place'], '',p[2], 'ARRAY')

	p[0] = {'type':exp_type, 'beginlist':[], 'endlist':[]}    

def p_arrayList(p):
	' arrayList : COMMA expression arrayList '

	if p[2]['type']=="TYPE ERROR":
		print "ERROR: line "+str(p.lineno(2))+" :expression in array assignment has type error\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = p[3]['type']

	p[3]['elements'].insert(0, {'type':p[2]['type']})
	p[0] = {'type':exp_type, 'elements':p[3]['elements']}

def p_arrayList_empty(p):
	' arrayList : COMMA expression '

	p[0]={'elements':[{'type':p[2]['type']}], 'type':'array'}
	if p[2]['type']=="TYPE ERROR":
		print "ERROR: line "+str(p.lineno(2))+" :expression in array assignment has type error\n"
		p[0]['type']="TYPE ERROR"
	

def p_expression_unary(p):								#INCREMENT_OP and DECREMENT_OP deleted
	''' expression : PLUS_OP expression   %prec UPLUS
				   | MINUS_OP expression  %prec UMINUS
				   | BIT_FLIP expression'''

	p[0] = {'place':symTable.newtmp()}

	if p[2]['type']!='NUMBER' :
		print "ERROR: line "+str(p.lineno(2))+" : Type error.\n"
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
		print "ERROR: line "+str(p.lineno(2))+" : Type error in expression.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], '', p[1], p[2]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']= str(p[1])+str(p[2]['value'])

def p_expression_unary_notStrOp(p):
	'expression : NOT_STR_OP expression'
	
	p[0] = {'place':symTable.newtmp(), 'truelist':p[2]['falselist'], 'falselist':p[2]['truelist']}
	if p[2]['type']!='BOOLEAN' :
		print "ERROR: line "+str(p.lineno(2))+" : Type error in expression.\n"
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
# def p_expression_bin_dig(p):
# 	'''expression :  expression XOR_STR_OP expression
# 					| expression COMPARE_OP expression
# 					| expression BIT_OR expression
# 					| expression BIT_XOR expression
# 					| expression BIT_AND expression'''


def p_exp_and_str_op(p):
	'expression : expression AND_STR_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'falselist':threeAddrCode.merge(p[1]['falselist'], p[4]['falselist']), 'truelist':p[4]['truelist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "ERROR: line "+str(p.lineno(2))+" : Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['truelist'], p[3]['quad'])
	p[0]['type']=exp_type

def p_exp_and_op(p):
	'expression : expression AND_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'falselist':threeAddrCode.merge(p[1]['falselist'], p[4]['falselist']), 'truelist':p[4]['truelist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "ERROR: line "+str(p.lineno(2))+" : Illegal expression\n"
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
		print "ERROR: line "+str(p.lineno(2))+" : Illegal expression\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[4]['place'])

	threeAddrCode.backpatch(p[1]['falselist'], p[3]['quad'])
	p[0]['type']=exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[4]['value'])

def p_exp_or_str_op(p):
	'expression : expression OR_STR_OP Marker expression'

	p[0] = {'place':symTable.newtmp(), 'truelist':threeAddrCode.merge(p[1]['truelist'], p[4]['truelist']), 'falselist':p[4]['falselist']}
	if p[1]['type']!='BOOLEAN' or p[4]['type']!='BOOLEAN' :
		print "ERROR: line "+str(p.lineno(2))+" : Illegal expression\n"
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
		print "ERROR: line "+str(p.lineno(2))+" : cannot compare\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "BOOLEAN"

	p[0] = {'type' : exp_type, 'place':symTable.newtmp(), 'truelist':[], 'falselist':[]}
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
		print "ERROR: line "+str(p.lineno(2))+" : cannot perform operation\n"
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
		print "ERROR: line "+str(p.lineno(2))+" : How many times to repeat?.\n"
		exp_type = "TYPE ERROR"
	elif p[1]['type']!='STRING' :
		print "ERROR: line "+str(p.lineno(2))+" : You can only repeat a string.\n"
		exp_type = "TYPE ERROR"
	else:
		exp_type = "STRING"
		threeAddrCode.emit(p[0]['place'], p[1]['place'], p[2], p[3]['place'])

	p[0]['type'] = exp_type
	# p[0]['value']=str(p[1]['value'])+str(p[2])+str(p[3]['value'])

## SAB KUCHH ACHCHHE SE DEKHO ISME
# def p_expression_binary(p):
# 	'''expression 	: expression ASSOCIATE_OP expression
# 					| expression RANGE_OP expression
# 					| expression SEARCH_MODIFY expression
# 					| expression SEARCH_MODIFY_NEG expression'''



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


def scopecode(name,taccode):
	global code_string
	global data_strings
	global cod_strings
	global global_vars
	global print_flag
	# print "cwjnewgjmn"
	if name!="root1":
		code_string+=name+":\n"
		code_string+="pushl %eax\npushl %ecx\npushl %edx\npushl %edi\npushl %esi\n"
	code_string+="pushl"+"\t"+"%ebp\n"
	code_string+="movl"+"\t"+"%esp"+","+"%ebp\n"
		
	offset=0
	for TAC in taccode[name]:
		try:
			code_string+= TAC[4]+":\n"
		except IndexError:
			code_string+= ""


		if TAC[2]=="=":	

			print global_vars
			print "11111111111111112222222222222222222222222"		
			if type(TAC[3]) is int:
				flag=0
				offset=offset-4
				code_string+= "movl"+"\t$"+str(TAC[3])+","+str(offset)+"(%ebp)\n"
				temp_key=str(TAC[0])
				temp_add[temp_key]=str(offset)+"(%ebp)"
				# print TAC[0]
				# print temp_add[TAC[0]]
				# num_value_temp=TAC[3]
			elif re.match(r'"*"',TAC[3]):
				flag=1
				global_vars[TAC[0]]="STRING"
				string_value_temp=re.match(r'\"(.*)\"',TAC[3]).group(1)
				data_strings[TAC[0]]=TAC[0]+":\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0] \
					+"_len = . - "+TAC[0]
				global_strings[TAC[0]] = re.match(r'\"(.*)\"',TAC[3]).group(1)
				cod_strings[TAC[0]]=TAC[3]
			elif re.match(r'\'(.*)\'',TAC[3]):
				flag=1
				global_vars[TAC[0]]="STRING"
				string_value_temp=re.match(r'\'(.*)\'',TAC[3]).group(1)
				data_strings[TAC[0]]=TAC[0]+":\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0]\
					+"_len = . - "+TAC[0]
				global_strings[TAC[0]]=re.match(r'\'(.*)\'',TAC[3]).group(1)
				cod_strings[TAC[0]]=TAC[3]
			elif re.match(r'\'*\'',TAC[3]):
				flag=1
				global_vars[TAC[0]]="STRING"
				string_value_temp=re.match(r'\'*\'',TAC[3]).group()
				data_strings[TAC[0]]=TAC[0]+":\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0]\
					+"_len = . - "+TAC[0]
				global_strings[TAC[0]]=re.match(r'\'*\'',TAC[3]).group()
				cod_strings[TAC[0]]=TAC[3]




			elif re.match(r'\$.*',TAC[3]):
				print TAC[3]
				print TAC[0]
				print "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
				if global_vars.has_key(TAC[3]):
					if global_vars[TAC[3]]=="NUMBER":
						flag=0
						offset=offset-4
						code_string+= "movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%edi\n"
						code_string+="movl\t%edi,"+str(offset)+"(%ebp)\n"
						temp_key=str(TAC[0])
						temp_add[temp_key]=str(offset)+"(%ebp)"
					else:
						flag=1
						global_vars[TAC[0]]="STRING"
						print global_strings
						string_value_temp=global_strings[str(TAC[3].split("$")[1])+"_str__ing__"]
						data_strings[TAC[0]]=TAC[0]+":\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0]\
							+"_len = . - "+TAC[0]
						# string_value_temp=".ascii\t\""+global_strings[str(TAC[3].split("$")[1])+"_str__ing__"]+"\"\n"
						# data_strings[TAC[0]]=TAC[0]+":\n"+string_value_temp+TAC[0]\
						# 	+"_len = . - "+TAC[0]
						global_strings[TAC[0]]=string_value_temp
						# cod_strings[TAC[0]]="\'"+global_strings[function_list_linear[TAC[3]]]+"\'"
				else:
					print "ERROR: Variable not available\n"
				# print TAC[0]
				# print temp_add[TAC[0]]
				# num_value_temp=TAC[3]

			elif function_list_linear.has_key(TAC[3]):
				print function_list_linear
				print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
				temp12=function_list_linear[TAC[3]]
				temp13=temp12.split('_')[0]
				if re.match(r'temp\d+',temp13):
					temp14=temp13
				else:
					temp14="$"+temp13
				print temp14
				print TAC[0]
				print symTable.symbolTable['root'][TAC[3]]['returntype']
				print "WWWWWWWWWWWWWWWWWWQQQQQQQQQQQQQQQQQQQQQQ"
				print global_vars
				if global_vars.has_key(temp14):
					print "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
					print global_vars[temp14]
					# if global_vars[symTable.symbolTable['root'][TAC[3]]['returntype']]=="NUMBER":
					if global_vars[temp14]=="NUMBER":
						flag=0
						offset=offset-4
						print "QWERTYUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
						code_string+= "movl\t"+function_list_linear[TAC[3]]+",%edi\nmovl\t%edi,"+str(offset)+"(%ebp)\n"
						temp_key=str(TAC[0])
						temp_add[temp_key]=str(offset)+"(%ebp)"
						# num_value_temp=TAC[3]
					else:
						print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
						print global_strings
						flag=1
						global_vars[TAC[0]]="STRING"
						# if backPatchingStrings.has_key(temp14):
						# 	backPatchingStrings[temp14].append(TAC[0])
						# else:
						# 	backPatchingStrings[temp14]=[TAC[0]]
						string_value_temp=global_strings[function_list_linear[TAC[3]]]
						data_strings[TAC[0]]=TAC[0]+":\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0]\
							+"_len = . - "+TAC[0]
						global_strings[TAC[0]]=global_strings[function_list_linear[TAC[3]]]
						cod_strings[TAC[0]]="\'"+global_strings[function_list_linear[TAC[3]]]+"\'"
				else:
					flag=0
					offset=offset-4
					code_string+= "movl\t%ebx,"+str(offset)+"(%ebp)\n"
					temp_key=str(TAC[0])
					temp_add[temp_key]=str(offset)+"(%ebp)"
					# print TAC[0]
					# print temp_add[TAC[0]]
					# num_value_temp=TAC[3]


			else:
				if flag==0:
					# print TAC[0]
					if re.match(r'\$.*',TAC[0]):
						data_strings[str(TAC[0].split('$')[1])+"_num__ber__"]=TAC[0].split('$')[1]+"_num__ber__:\n\t.long\t"+str(0)
						global_vars[TAC[0]]="NUMBER"
						get_offset=temp_add[str(TAC[3])]	
						code_string+= "movl"+"\t"+get_offset+","+"%edi\n"
						code_string+="movl\t%edi,"+TAC[0].split('$')[1]+"_num__ber__"+"\n"
					else:
						print "ERROR: "

				else:
					global_vars[TAC[0]]="STRING"
					global_strings[TAC[0].split('$')[1]+"_str__ing__"]=string_value_temp
					string_value_temp=TAC[0].split('$')[1]+"_str__ing__:\n.ascii\t\""+string_value_temp+"\"\n"+TAC[0].split('$')[1] \
					+"_len = . - "+TAC[0].split('$')[1]+"_str__ing__"
					data_strings[str(TAC[0].split('$')[1])+"_str__ing__"]=string_value_temp


###################EXIT##############################################################

		if TAC[2]=="EXIT":
			code_string+="movl\t$1,%eax\nmovl\t$0,%ebx\nint\t$0x80\n"
##################PRINT##############################################################
		if TAC[2]=="print":
			if TAC[0]=="NUMBER":###Deepak will give the function
				print_flag=1
				if re.match(r'\$.*', TAC[3]):
					code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__,%ecx\n"
					code_string+="call printIntNumber\n"
				else:
					print temp_add
					print "QWERTYUI!@#$%^&*()^&*("
					get_offset=temp_add[str(TAC[3])]	
					code_string+= "movl"+"\t"+get_offset+","+"%ecx\n"
					code_string+="call printIntNumber\n"
			elif TAC[0]=="STRING":
				code_string+="movl\t$4,%eax\nmovl\t$1,%ebx\n"
				# print "movl\t$4,%eax\nmovl\t$1,%ebx\n"
				# print TAC[3]
				# print "AAAAAAAAAAAAAAAAAAAAAAAAA"
				if re.search(r'\$',TAC[3]):
					code_string+="movl\t$"+TAC[3].split('$')[1]+"_str__ing__"+",%ecx\n"
					code_string+="movl\t$"+TAC[3].split('$')[1]+"_len,%edx\n"
					code_string+="int\t$0x80\n"
				else:
					code_string+="movl\t$"+TAC[3]+",%ecx\n"
					code_string+="movl\t$"+TAC[3]+"_len,%edx\n"
					code_string+="int\t$0x80\n"	
			elif TAC[0]=="RES_STRING":
				code_string+="movl\t$4,%eax\nmovl\t$1,%ebx\n"
				# print "movl\t$4,%eax\nmovl\t$1,%ebx\n"
				# print TAC[3]
				# print "AAAAAAAAAAAAAAAAAAAAAAAAA"
				if re.search(r'\$',TAC[3]):
					code_string+="movl\t$"+TAC[3].split('$')[1]+"_str__ing__"+",%ecx\n"
					code_string+="movl\t$"+TAC[3].split('$')[1]+"_len,%edx\n"
					code_string+="int\t$0x80\n"
				else:
					code_string+="movl\t$"+TAC[3]+",%ecx\n"
					code_string+="movl\t$"+TAC[3]+"_len,%edx\n"
					code_string+="int\t$0x80\n"	
			else:
				print "ERROR: You are trying to print the UNPRINTABLE :D\n"
#######################ADDITION######################################################

		if TAC[2]=="+":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="addl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="addl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[0]):
				code_string+="movl\t"+"%eax,"+TAC[1].split('$')[1]+"_num__ber__"+"\n"
			else:
				offset=offset-4
				code_string+= "movl"+"\t%eax,"+str(offset)+"(%ebp)\n"
				temp_key=str(TAC[0])
				temp_add[temp_key]=str(offset)+"(%ebp)"
############################SUBTRACTION###############################################
		
		if TAC[2]=="-":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="subl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="subl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[0]):
				code_string+="movl\t"+"%eax,"+TAC[1].split('$')[1]+"_num__ber__"+"\n"
			else:
				offset=offset-4
				code_string+= "movl"+"\t%eax,"+str(offset)+"(%ebp)\n"
				temp_key=str(TAC[0])
				temp_add[temp_key]=str(offset)+"(%ebp)"
		
######################################COMPARISON######################################
		
		if TAC[2]==">":
			
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"
			#code_string+="jg\ttrue\n"
			# if TAC[0] in global_vars:
			# 	code_string+="movl\t"+"%eax,"+TAC[1].split('$')[1]+"\n"
			# else:
			# 	offset=offset-4
			# 	code_string+= "movl"+"\t%eax,"+str(offset)+"(%ebp)\n"
			# 	temp_key=str(TAC[0])
			# 	temp_add[temp_key]=str(offset)+"(%ebp)"



		if TAC[2]=="<":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"

		if TAC[2]==">=":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"



		if TAC[2]=="<=":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"



		if TAC[2]=="==":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"


		if TAC[2]=="!=":
			if global_vars.has_key(TAC[1]):
				code_string+="movl\t"+TAC[1].split('$')[1]+"_num__ber__"+",%eax\n"
			else:
				get_offset=temp_add[str(TAC[1])]
				code_string+="movl\t"+get_offset+",%eax\n"
			if global_vars.has_key(TAC[3]):
				code_string+="movl\t"+TAC[3].split('$')[1]+"_num__ber__"+",%ebx\n"
			else:
				get_offset=temp_add[str(TAC[3])]
				code_string+="movl\t"+get_offset+",%ebx\n"
			temp_operator=TAC[2]
			code_string+="cmpl\t%eax,%ebx\n"

##################################CONDITIONALGOTO#####################################

		if TAC[2]=="FALSE_GOTO":
			if temp_operator==">":
				code_string+= "jg\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<":
				code_string+= "jl\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator==">=":
				code_string+= "jge\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<=":
				code_string+= "jle\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="==":
				code_string+= "jne\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="!=":
				code_string+= "je\t"+"label_"+str(TAC[3])+"\n"
			else:
				code_string+=""

		if TAC[2]=="GOTO_MARK":
			if temp_operator==">":
				code_string+= "jg\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<":
				code_string+= "jl\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator==">=":
				code_string+= "jge\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<=":
				code_string+= "jle\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="==":
				code_string+= "jne\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="!=":
				code_string+= "je\t"+"label_"+str(TAC[3])+"\n"
			else:
				code_string+=""


		if TAC[2]=="GOTO_MARK2":
			if temp_operator==">":
				code_string+= "jle\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<":
				code_string+= "jge\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator==">=":
				code_string+= "jl\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="<=":
				code_string+= "jg\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="==":
				code_string+= "je\t"+"label_"+str(TAC[3])+"\n"
			elif temp_operator=="!=":
				code_string+= "jne\t"+"label_"+str(TAC[3])+"\n"
			else:
				code_string+=""


###############################GOTO####################################################

		if TAC[2]=="GOTO":
			code_string+="jmp\tlabel_"+str(TAC[3])+"\n"
		if TAC[2]=="GOTO_END":
			code_string+="jmp\tlabel_"+str(TAC[3])+"\n"

################################FUNCTION###################################################


		if TAC[2]=="GOTO_LABEL":
			code_string+="call "+str(TAC[3])+"\n"

		if TAC[2]=="return":
			if global_vars.has_key(TAC[0]):
				if global_vars[TAC[0]]=="NUMBER":
					function_list_linear[name]=TAC[0].split('$')[1]+"_num__ber__"
				else:
					if re.match(r'\$.*', TAC[0]):
						# print TAC[0]
						# print "TTTTT"
						function_list_linear[name]=TAC[0].split('$')[1]+"_str__ing__"
					else:
						function_list_linear[name]=TAC[0]

						# for target in backPatchingStrings[TAC[0]]:
						# 	string_value_temp = global_strings[TAC[0]]
						# 	data_strings[target]=target+":\n.ascii\t\""+string_value_temp+"\"\n"+target\
						# 		+"_len = . - "+target+"\n"
						# 	global_strings[target]=global_strings[TAC[0]]

			else:
				get_offset=temp_add[str(TAC[0])]	
				code_string+= "movl"+"\t"+get_offset+","+"%ebx\n"
			code_string+="movl"+"\t"+"%ebp"+","+"%esp\n"
			code_string+="popl\t%ebp\n"
			code_string+="popl %esi\npopl %edi\npopl %edx\npopl %ecx\npopl %eax\nret\n"
			
			

		if TAC[2]=="JUMP_CALLING":
			# code_string+="pushl"+"\t"+"%ebp\n"
			code_string+="movl"+"\t"+"%ebp"+","+"%esp\n"
			code_string+="popl\t%ebp\n"
			code_string+="popl %esi\npopl %edi\npopl %edx\npopl %ecx\npopl %eax\nret\n"

			symTable.symbolTable['root'][name]['returntype']="VOID"
			

		# if TAC[2]=="FUNC_LABEL":
		# 	code_string+=str(TAC[3])+":\n"

def genasm(taccode):
	
	flag=0
	# num_value_temp=0	
	offset=0
	temp_operator="=="
	for item in function_list:
		for i in function_list[item]:
			scopecode(i,taccode)
	
def write_into_file(name, Str_to_write):
	try:
		myfile = open(name, 'w')
		myfile.write(Str_to_write)
		myfile.close()
	except:
		print "ERROR: Somehow the file"+str(name)+"could not be generated\n"
		sys.exit(0)

def format_symTable(hashName, work_string, depth):
	for element in hashName:
		# print element
		# print hashName[element]
		if isinstance(element, dict):
			depth+=1;
			work_string+=format_symTable(element, work_string, depth)
		else:
			for x in xrange(1,depth):
				work_string+="\t"
			work_string+= "\t"+str(element)+" : "+str(hashName[element])+"\n"
	return work_string

def runparser(inputfile):
	global code_string
	global data_string
	global data_strings
	global print_flag
	program=open(inputfile).read()
	result=parser.parse(program,lexer=lexer, debug=0)
	# print result
	print "\nGenerating Symbol Table ...\n"
	# print symTable.symbolTable
	symbol_table_string = ""
	for scopes in symTable.symbolTable:
		symbol_table_string += format_symTable(symTable.symbolTable[scopes], symbol_table_string, 0)

	write_into_file("symbolTable.gen", symbol_table_string)
	print "\nGenerating Three Address Code...\n"
	# print threeAddrCode.code
	threeAddrCode_string = ""
	for scopes in threeAddrCode.code:
		count = 0
		# print "In the scope "+str(scopes)+" :-"
		threeAddrCode_string+= "In the scope "+str(scopes)+" :-\n"

		for TAC in threeAddrCode.code[scopes]:
			# print "\t"+str(count)+"\t"+str(TAC)
			threeAddrCode_string+= "\t"+str(count)+"\t"+str(TAC)+"\n"
			count+=1
	write_into_file("Three_Address_Code.gen", threeAddrCode_string)


	for scopes in threeAddrCode.code:
		count = 0
		for TAC in threeAddrCode.code[scopes]:
			if TAC[2]=="FALSE_GOTO":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="GOTO_END":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="GOTO_SWITCH":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="GOTO":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="GOTO_MARK":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="GOTO_MARK2":
				temp=TAC[3]
				temp1="label_"+str(temp)
				threeAddrCode.code[scopes][temp].append(temp1)
			if TAC[2]=="return":
				temp = re.match(r'\$(.*)',TAC[0])
				if temp:
					if symTable.symbolTable['root'][scopes]['returntype']=="NUMBER":
						global_vars[TAC[0]]="NUMBER"
						function_list_linear[scopes]=str(temp.group(1))+"_num__ber__"
					elif symTable.symbolTable['root'][scopes]['returntype']=="STRING":
						global_vars[TAC[0]]="STRING"
						function_list_linear[scopes]=str(temp.group(1))+"_str__ing__"
					elif symTable.symbolTable['root'][scopes]['returntype']=="RES_STRING":
						global_vars[TAC[0]]="STRING"
						function_list_linear[scopes]=str(temp.group(1))+"_str__ing__"
					else:
						print "ERROR: You cannot return values in VOID functions\n\tYou returned value of type: "+symTable.symbolTable['root'][scopes]['returntype']+"\n"
				else:
					function_list_linear[scopes]=TAC[0]
					global_vars[TAC[0]]="STRING"      # Because in case of Numbers, we will not use the global


			count+=1

	# for scopes in threeAddrCode.code:
	# 	count = 0
	# 	print "In the scope "+str(scopes)+" :-"

	# 	for TAC in threeAddrCode.code[scopes]:
	# 		print "\t"+str(count)+"\t"+str(TAC)
	# 		count+=1
	print global_strings
	print "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[["
	for item in global_strings:
		print global_strings[item]
		print "____________________________"
		if not isinstance(global_strings[item],int):
			if re.match(r'\'(.*)\'',global_strings[item]):
				print "XXXXXXXXXXXXXXXXXXXXXXXX"
				global_strings[item]=re.match(r'\'(.*)\'',global_strings[item]).group(1)
			if re.match(r'\"(.*)\"',global_strings[item]):
				print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
				global_strings[item]=re.match(r'\"(.*)\"',global_strings[item]).group(1)
	genasm(threeAddrCode.code)
	print function_list
	print function_list_linear
	print "qwertyuiopasdfghjklzxcvbnm"
	print global_vars
	for item in data_strings:
		code_string = data_strings[item]+"\n"+code_string
	code_string = data_string+ code_string
	if print_flag==1:
		code_string += printIntCode  #Append the line to print the code of the printing number

	print "\nGenerating x86 Assembly Code...\n"
	# print code_string
	write_into_file("output.s", code_string)

	os.system("as -32 output.s -o output.o")
	os.system("ld -m elf_i386 output.o -o output")

if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runparser(inputfile)
