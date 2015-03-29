class SymbolTable:
	def __init__(self):
		self.symbolTable = {
			'root' :{
				'scope' : 'root1',
				'parent': 'root1',
				'type' : 'FUNCTION',
				'returntype' : 'UNDEFINED',
				'string_list': [],
				'width' : '0',
				'scope_depth': 0
			}
		}
		#########Two stacks for offset and scope of the variable
		self.offset=[0]
		self.entryscope=[self.symbolTable['root']]
		
		self.address_size=4
		self.boolean_size=1
		self.integer_size=4
		self.float_size=8
		self.char_size=1
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
		curr=self.entryscope(len(self.entryscope)-1)
		name="\'"+name+"\'"
		print name
		curr[name]=value
	

	def ifexist(self,entry):
		entry=self.lookup(entry)
		if entry != None
			return True
		else:
			return False


	def getvalueofkey(self,entry,key):
		entry=self.lookup(entry)
		if entry.has_key("\'"+key+"\'"):
			return entry["\'"+key+"\'"]
		else: 
			None

