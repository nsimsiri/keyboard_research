from csvhandler import CSVHandler

class OverloadTable(object):
	def __init__(self, filedir=None):
		#if filedir==None: filedir = 'overload_final_1.csv'
		if filedir==None: filedir = 'overload_final_2.csv'
		#if filedir==None: filedir = 'overload_final_3.csv'
		overload_file = CSVHandler(filedir)
		table_list = overload_file.get_list()
		self._table = dict()
		for row in table_list:
			self._table[row[0].decode('utf-8')] = [elm.decode('utf-8') for elm in row[1:]]

	def __str__(self):
		overloadstring = str()
		for table_key in self._table.keys():
			overloadstring += '%s:'%(table_key.encode('utf-8'))
			for key in self._table[table_key]:
				overloadstring += ' => %s'%key.encode('utf-8')
			overloadstring += '\n'
		return overloadstring

	def has_overloaded_key(self, overload_key):
		'''is key in the overloaded stack? | is it one of ovl_n {key: [ovl_1, ovl_2...]}'''
		for table_key in self._table:
			if overload_key in self._table[table_key]: return True
		return False

	def has_key(self, key): return key in self._table 

	def get_keys_from_overloaded_key(self, foreign_key):
		'''get list of possible overloaded key it belongs to'''
		overloaded_keys = []
		for table_key in self._table.keys():
			if foreign_key in self._table[table_key]:
				overloaded_keys.append(table_key)
		return overloaded_keys

	def get_tap_count(self, key, foreign_key):
		if (self.has_key(key)):
			if (self.has_overloaded_key(foreign_key)):
				return self._table[key].index(foreign_key) + 1
		return 0

	def get_tablekeys(self): return self._table.keys()
	def get_overloadedkeys(self, key): return self._table[key]

if __name__ == '__main__':
	table = OverloadTable()
	keylist = table.get_tablekeys()
	overloadedkeys = []
	for elm in keylist: 
		#print elm
		overloadedkeys+=table.get_overloadedkeys(elm)
	print ('---\n')
	for elm in overloadedkeys:
		top_keys = table.get_keys_from_overloaded_key(elm)
		for top in top_keys: 
			print('%s <- %s'%(top, elm))
	# 	print elm




