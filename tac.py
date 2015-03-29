class Tac:
	def __init__(self,symTable):
		self.code={'root1':[]}
		self.quad={'root1':-1}
		self.quad_next={'root1':0}
		self.symTable=symTable

	def quad_increment(self):
		curr=self.symTable.get_current_scope()
		self.quad[curr]=self.quad_next[curr]
		self.quad_next[curr]=self.quad[curr]+1
		return self.quad[curr]

	def pointer_quad_next(self):
		curr=self.symTable.get_current_scope()
		return self.quad_next[curr]

	def emit(self,rt,lt1,op,lt2):
		curr=self.symTable.get_current_scope()
		self.quad_increment()
		self.code[curr].append([rt,lt1,op,lt2])

	def merge(self,p1,p2):
		p3=p1+p2
		return p3

	def backpatch(self,p,i):
		curr=self.symTable.get_current_scope()
		for j in p:
			self.code[curr][j]=i