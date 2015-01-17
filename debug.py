import pprint

class debug:
	def __init__(self):
		self.showerrormsg=False
		self.printerror=True
		self.linenumber=1

	def printerror(self,statement):
		if self.printerror:
			print 'Error '
