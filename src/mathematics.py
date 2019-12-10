import random

class Excercise:
	def __init__(self):
		self.a = None
		self.b = None
		self.ans = None
	
	def check_ans(self, ans):
		op = False
		if self.ans == ans:
			op = True
		else:
			False
		return op

class ShortSum(Excercise):
	def __init__(self):
		Excercise.__init__(self)

	def generate(self):
		opt = True 
		while opt:
			self.a = random.randint(0,999)
			print self.a
			self.b = random.randint(0,999)
			if self.a + self.b > 999:
				opt = True
			else:
				opt = False
		self.ans = self.a + self.b
	

class ShortDif(Excercise):
	def __init__(self):
		Excercise.__init__(self)
	
	def generate(self):
		opt = True 
		while opt:
			self.a = random.randint(0,999)
			self.b = random.randint(0,999)
			if self.b > self.a:
				opt = True
			else:
				opt = False
		self.ans = self.a - self.b
	
class ShortProd(Excercise):
	def __init__(self):
		Excercise.__init__(self)
	
	def generate(self):
		opt = True
		while opt:
			self.a = random.randint(0,999)
			self.b = random.randint(0,99)
			if self.a * self.b > 999:
				opt = True
			else:
				opt = False	
		self.ans = self.a * self.b

class ShortDiv(Excercise):
	def __init__(self):
		Excercise.__init__(self)

	def generate(self):
		opt = True
		while opt:
			self.a = random.randint(1,999)
			self.b = random.randint(1,10)
			if self.a % self.b != 0:
				opt = True
			else:
				opt = False
		self.ans = self.a / self.b

def main():
	sm = ShortDiv()
	sm.generate()
	print "ejercicio %i + %i = " %(sm.a,sm.b)
	if sm.check_ans(int(raw_input())):
		print "bien"
	else:
		print "nlm"
	print "la respuesta correcta es: %i" %(sm.ans)	
if __name__=="__main__": main() 
