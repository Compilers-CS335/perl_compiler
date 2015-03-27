class SymbolTable:
	def __init__(self):
		self.symbolTable {
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


	