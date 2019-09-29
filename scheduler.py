class Scheduler():
	"""
	Scheduler for PyWar piece operations.
	"""
	def __init__(self):
		"""
		Initialize the scheduler
		"""
		self.operations = {}
	
	@property
	def jobs(self):
		"""
		Fetches the list of job ids running
		"""
		return self.operations.keys()
	
	def _touch(self, job_id):
		if job_id not in self.jobs:
			self.operations[job_id] = []
	
	def add_meta(self, job_id, meta):
		"""
		Stores extra metdata on the queue
		:param job_id: the job_id
		:type job_id: Seralizable
		:param meta: the metadata to be stored
		:type meta: object. Not tuple and not list.
		"""
		if isinstance(meta, tuple) or isinstance(meta, list):
			return
		
		self._touch(job_id)
		self.operations[job_id].append(meta)
	
	@staticmethod
	def append_to_list(lst, func, params, repeat=True):
		"""
		Formats a list to match the queue
		:param lst: list of jobs
		:type lst: list
		:param func: the function to queue
		:type func: function
		:param params: a dictionary of params to be passed
		:type params: dict
		:param repeat: Wether the job should be repeating
		:type repeat: bool
		"""
		lst.append((func, repeat, params))
		
	
	def add(self, job_id, func, params, repeat=True):
		"""
		Appends task to job_id
		:param job_id: the job_id
		:type job_id: Seralizable
		:param func: the function to queue
		:type func: function
		:param params: a dictionary of params to be passed
		:type params: dict
		:param repeat: Wether the job should be repeating
		:type repeat: bool
		"""
		self._touch(job_id)
		self.operations[job_id].append((func, repeat, params))
	
	def isbusy(self, job_id):
		"""
		Checks if a job_id has tasks queued
		:param job_id: the job_id
		:type job_id: Seralizable
		"""
		return job_id in self.operations.keys()
		
	def flush(self, job_id):
		"""
		Clears the job's queue
		:param job_id: the job_id
		:type job_id: Seralizable
		"""
		self.operations.pop(job_id, None)
	
	def clean(self):
		"""
		Removes empty job_ids
		"""
		for job in self.jobs:
			if len(self.operations[job]) == 0:
				self.flush(job)
	
	def run(self, new_data):
		"""
		Runs a turn out of each job_id
		:param new_data: first object in method call (usually self) used to update params
		:type new_data: object
		"""
		for job in self.jobs:
			while len(self.operations[job]) > 0 and not isinstance(self.operations[job][0], tuple):
				self.operations[job].pop(0)
			if len(self.operations[job]) == 0:
				continue
			func, repeat, params = self.operations[job][0]
			ret = func(new_data, **params)
			if not isinstance(ret, bool):
				self.operations[job] = ret + self.operations[job][1:]
			else:
				if ret or not repeat:
					self.operations[job].pop(0)
		for job in self.jobs:
			while len(self.operations[job]) > 0 and not isinstance(self.operations[job][0], tuple):
					self.operations[job].pop(0)
		self.clean()

class Test():
	def __init__(self, a):
		self.a = a
	
	def print_a(self):
		print(self.a)
		return True
	
	def double_print(self, b):
		lst = []
		Scheduler.append_to_list(lst, Test.print_a, {}, False)
		Scheduler.append_to_list(lst, Test.print_ab, {"b": b}, True)
		return lst
	
	def print_ab(self, b):
		print(self.a, b)
		return self.a==5

my_scheduler = Scheduler()
my_scheduler.add(1, Test.double_print, {"b": 9})
for i in range(10):
	print(my_scheduler.operations)
	my_scheduler.run(Test(i))
