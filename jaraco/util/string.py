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