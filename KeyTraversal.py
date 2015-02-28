class KeyTraversalTable(object):
	''' abstraction of a dictionary such that keys are edges (n1, n2) and values are (path, freq)
		where paths are List[TupleTuple(String, String), Int)] - should abstract this, but no time. 
	'''
	def __init__(self):
		self.table = dict()
		self._keys=[]
		self.rawpath=[]
	def __str__(self): 
		tablstring = str()
		for edge in self._keys:
			e0, e1 = edge[0], edge[1]
			if (type(e0)==unicode): e0=e0.encode('utf-8')
			if (type(e1)==unicode): e1=e1.encode('utf-8') 
			tablstring += '(%s, %s): %s\n'%(e0, e1,(self.table[edge]))
		return tablstring
	def __len__(self): return len(self.table)
	def __contains__(self, edge): return self.has_edge(edge)
	def append(self, edge, path, isOverload=False):
		if (type(edge)!=tuple): raise TypeError("KeyTraversalTable: Key not a Tuple!")
		if (len(edge)!=2): raise ValueError("KeyTraversalTable: Key must be an edge of 2 nodes (n1, n2)")

		if (not(edge in self.table)):
			self.table[tuple(edge)] = KeyPathData(path, isOverload=isOverload)
		else:
			traversaldata = self.table[tuple(edge)]
			traversaldata.increment_freq()
		self._keys.append(edge)

	def get_edges(self): return self.table.keys()
	def get_keypathdata(self, edge): return self.table[edge]
	def get_distance(self):
		distance=0
		for edge in self.table:
			distance+=int(self.table[edge].pathdistance()*self.table[edge].freq())
		return distance
	def get_keypresscount(self):
		count=0
		for edge in self.table:
			count+=int(self.table[edge].keypresscount()*self.table[edge].freq())
		return count

	def has_edge(self, edge): 
		if (type(edge)==tuple and len(edge)==2):
			return edge in self.table
		else: raise ValueError("Not an edge.")

	def get_seekcount(self):
		seek_count = 0
		for edge in self.table:
			seek_count+=int(self.table[edge].seekcount()*self.table[edge].freq())
		return seek_count


class KeyPathData(object):
	def __init__(self, path, isOverload=False):
		if (len(path)!=0): 
			for a_path in path: 
				if (type(a_path)!=tuple): raise TypeError("Element of path not a tuple.")
				if (type(a_path[0])!=tuple): raise TypeError("a path does not contain an edge of tuple.")
				if (len(a_path)!=2 or len(a_path[0])!=2): raise TypeError("Does not contain proper number of elements in a path.")
				try:
					if (type(int(a_path[1])) != int): raise TypeError()
				except: 
					raise TypeError('distance element not an integer')
		self._path = path
		self._freq = 1
		self._isOverload = isOverload
	def __len__(self): return len(self._path)
	def __str__(self):
		start=True
		pathstring=str()
		for a_path in self._path:
			from_node, to_node, distance = a_path[0][0], a_path[0][1], a_path[1]
			if (type(from_node)==unicode): from_node=from_node.encode('utf-8')
			if (type(to_node)==unicode): to_node=to_node.encode('utf-8')
			if (type(distance)==unicode): distance=distance.encode('utf-8')
			if (start): 
				start=False
				pathstring+='%s = [%s] => %s'%(from_node, distance, to_node)
			else:
				pathstring+=' = [%s] => %s'%(distance,to_node)
		pathstring = (pathstring + ' (freq= %i)'%(self._freq))
		if self.is_overloaded(): pathstring += ' (overloaded)'
		return pathstring
	def is_overloaded(self): return self._isOverload
	def increment_freq(self): self._freq+=1
	def get_rawpath(self): return self._path
	def get_path(self):
		path_edges=[]
		for path_edge_index in range(len(self._path)):
			((from_node, to_node), dist) = self._path[path_edge_index] ## get a path_edge 
			if (path_edge_index==0): path_edges += [from_node, to_node]
			else: path_edges += [to_node]
		return path_edges
	def freq(self): return self._freq
	def pathdistance(self):
		distance = 0
		for a_path_edge in self._path:
			distance += int(a_path_edge[1])
		return distance
	def keypresscount(self): return len(self)
	def seekcount(self):
		seek_count = 0
		for a_path_edge in self._path:
			dist = int(a_path_edge[1])
			if dist>0: seek_count+=1
		return seek_count




if (__name__ == '__main__'):
	key1 = ('a','c')
	path1 = [(('a', 'b'), 5), (('b','c'), 2)]

	key2 = ('c','a')
	path2 = [(('c', 'b'), 5), (('b','d'), 2), (('d', 'a'), 10)]

	key3 = ('a','c')
	path3 = [(('a', 'b'), 5), (('b','c'), 2)]

	key4 = (u'\u0e15', u'\u0e0f')
	path4 = [((u'\u0e15', u'\u0e15'), 0), ((u'\u0e15', u'\u0e0f'), 0)]

	travTabl = KeyTraversalTable()
	travTabl.append(key1, path1)
	travTabl.append(key1, path1)
	travTabl.append(key4, path4, isOverload=True)
	print (travTabl.__str__())
	for edge in travTabl.get_edges():
		a_pathdata = travTabl.get_keypathdata(edge)
		print 'dist: %i'%a_pathdata.pathdistance()
		print 'count: %i'%a_pathdata.keypresscount()
		print 'freq: %i'%a_pathdata.freq()
		print 'path: %s'%str(a_pathdata.get_rawpath())
		print 'seek: %i'%a_pathdata.seekcount()
		pathedgestring = ''
		for path_edge in a_pathdata.get_path(): 
			pathedgestring += '%s -> '%path_edge
		print pathedgestring

	assert (key1 in travTabl)
	assert (not (key2 in travTabl))



