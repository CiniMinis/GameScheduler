import scheduler

class Test():
	def __init__(self, a):
		self.a = a
	
	def print_a(self):
		print(self.a)
		return True
	
	def double_print(self, b):
		lst = []
		scheduler.Scheduler.append_to_list(lst, Test.print_a, {}, False)
		scheduler.Scheduler.append_to_list(lst, Test.print_ab, {"b": b}, True)
		return lst
	
	def print_ab(self, b):
		print(self.a, b)
		return self.a==5

my_scheduler = scheduler.Scheduler()
my_scheduler.add(1, Test.double_print, {"b": 9})
for i in range(10):
	print(my_scheduler.operations)
	my_scheduler.run(Test(i))
