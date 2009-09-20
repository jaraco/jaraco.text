import re
from itertools import starmap
from jaraco.util.functools import compose

def substitution(old, new):
	"""
	Return a function that will perform a substitution on a string
	"""
	return lambda s: s.replace(old, new)

def multi_substitution(*substitutions):
	"""
	Take a sequence of pairs specifying substitutions, and create
	a function that performs those substitutions.
	
	>>> multi_substitution(('foo', 'bar'), ('bar', 'baz'))('foo')
	'baz'
	"""
	substitutions = starmap(substitution, substitutions)
	# compose function applies last function first, so reverse the
	#  substitutions to get the expected order.
	substitutions = reversed(tuple(substitutions))
	return compose(*substitutions)

class FoldedCase(str):
	"""
	A case insensitive string class; behaves just like str
	except compares equal when the only variation is case.
	>>> s = FoldedCase('hello world')

	>>> s == 'Hello World'
	True

	>>> 'Hello World' == s
	True

	>>> s.index('O')
	4

	>>> s.split('O')
	['hell', ' w', 'rld']

	>>> sorted(map(FoldedCase, ['GAMMA', 'alpha', 'Beta']))
	['alpha', 'Beta', 'GAMMA']
	"""
	def __lt__(self, other):
		return self.lower() < other.lower()
	def __gt__(self, other):
		return self.lower() > other.lower()
	def __eq__(self, other):
		return self.lower() == other.lower()
	def __hash__(self):
		return hash(self.lower())
	# cache lower since it's likely to be called frequently.
	def lower(self):
		self._lower = super(FoldedCase, self).lower()
		self.lower = lambda: self._lower
		return self._lower

	def index(self, sub):
		return self.lower().index(sub.lower())

	def split(self, splitter=' ', maxsplit=0):
		pattern = re.compile(re.escape(splitter), re.I)
		return pattern.split(self, maxsplit)
