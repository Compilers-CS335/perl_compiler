class SymbolTable:
	def __init__(self):
		self.symbolTable = {
			'root' :{
				'scope' : 'root1',
				'parent': 'root1',
				'type' : 'FUNCTION',
				'returntype' : 'UNDEFINED',
				'scope_depth': 0
			}
		}
# scope=hello
# parent=currentscope ka parent
# type= integer
# return type=UNDEFINED
# width=4 





		#########Two stacks for offset and scope of the variable
		self.offset=[0]
		self.entryscope=[self.symbolTable['root']]
		
		self.proclist={ 'root': self.symbolTable['root']}
		self.temp_count=0
		self.temp_name_gen="temp"
		self.temp_vars = {}

	def newtmp(self):
		self.temp_count+=1
		temp_name=self.temp_name_gen+str(self.temp_count)
		self.temp_vars[temp_name]={'value': 0,
								   'scope': self.get_current_scope() }
		return temp_name

	def get_current_scope(self):
		return self.entryscope[len(self.entryscope)-1]['scope']

	def lookup(self,entry):

		return self.lookup_scope(entry,len(self.entryscope)-1)

	def lookup_scope(self,entry,location):
		if location==-1:
			
			return None

		scope_now=self.entryscope[location]
		
		if scope_now.has_key(entry):
			return scope_now[entry]

		else :
			return self.lookup_scope(entry,location-1)

	def addintocurrentscope(self,name,value):
		curr=self.entryscope[len(self.entryscope)-1]
		# name="\'"+name+"\'"
		# print name
		curr[name]=value
		current=self.entryscope[0]
		current[self.get_current_scope()][name]=value
	

	def ifexist(self,entry):
		entry=self.lookup(entry)
		if entry != None:
			return True
		else:
			return False


	def getvalueofkey(self,entry,key):
		entry=self.lookup(entry)
		if entry.has_key(key):
			return entry[key]
		else: 
			None


	def enterproc(self,name):
		curr=self.entryscope[len(self.entryscope)-1]
		temp=curr['scope_depth']+1
		curr[name]={
				'scope' : name,
				'parent': curr['scope'],
				'type' : 'FUNCTION',
				'returntype' : 'UNDEFINED',
				'scope_depth': temp
		}
		self.entryscope.append(curr[name])	
		self.proclist[name]=curr[name]
		self.offset.append(0)
		current=self.entryscope[0]
		current[name]['scope_depth']=temp


	def newvariableentry(self,varible,variabletype,isPrivate):
		# To set the scope of the variable correctly
		if isPrivate:
			curr=self.entryscope[len(self.entryscope)-1]
			# print curr
		else:
			curr=self.entryscope[0]
			# print curr

		
		if not (curr.has_key(varible)):
			curr[varible]={}

		if variabletype=="NUMBER":
			tempwidth=4
		elif variabletype=="STRING":
			tempwidth=8
		elif variabletype=="RES_STRING":
			tempwidth=8
		elif variabletype=="FUNCTION":
			tempwidth=8
		elif variabletype=="BOOLEAN":
			tempwidth=1
		else :
			tempwidth=0

		
		curr[varible]['type']=str(variabletype)
		curr[varible]['scope']=curr['scope']
		curr[varible]['width']=tempwidth
		curr[varible]['returntype']="UNDEFINED"

		temp1=self.offset.pop()
		temp1=temp1+tempwidth
		self.offset.append(temp1)

	def  getvalueofkey_variable(self,varible,value):
		entry=self.lookup(varible)
		if entry==None:
			return None
		if entry.has_key(value):
			return entry[value]
		else:
			return  None

	
	def removehash(self,name):
		self.entryscope.remove(name)

	def deletescope(self,procname):
		curr=self.entryscope.pop()
		curr['width']=self.offset.pop()


#########
	def newarrayentry(self,place,elements,isPrivate):
		# To set the scope of the variable correctly
		if isPrivate:
			curr=self.entryscope[len(self.entryscope)-1]
			# print curr
		else:
			curr=self.entryscope[0]
			# print curr


		if curr.has_key(place)==0:
			curr[place]={}

		curr[place]['type']='array'
		curr[place]['scope']=curr['scope']
		curr[place]['returntype']="UNDEFINED"
		curr[place]['elements']=elements

		tempwidth = 0;

		for element in curr[place]['elements']:
			
			if element['type']=="NUMBER":
				tempwidth+=4
				element['width']= 4
			elif element['type']=="STRING":
				tempwidth+=8
				element['width']= 8
			elif element['type']=="RES_STRING":
				tempwidth+=8
				element['width']= 8
			elif element['type']=="FUNCTION":
				tempwidth+=8
				element['width']= 8
			elif element['type']=="BOOLEAN":
				tempwidth+=1
				element['width']= 1
			else :
				tempwidth=0
				element['width']= 0

		# tempwidth=num_elem*tempwidth
		curr[place]['width']=tempwidth

		temp1=self.offset.pop()
		temp1=temp1+tempwidth
		self.offset.append(temp1)

	def  getvalueofkey_array(self,place,index,value):
		entry=self.lookup(place)
		if entry==None:
			return None
		if entry.has_key('elements'):
			if index>=len(entry['elements']):
				return None
			else:
				if entry['elements'][index].has_key(value):
					return entry['elements'][index][value]
				else:
					return None
		else:
			return  None	
