class A(object):
	def __init__(self, a):
		self.a = a
	def geta(self):
		return (self.a)

class B(A):
	def __init__(self, a, b):
		A.__init__(self, a)
		self.b = b
	def geta(self):
		a = super(B, self).geta()*2 
		return (a+self.b) #2a+b
	
ao = B(1,2)
print(ao.geta())