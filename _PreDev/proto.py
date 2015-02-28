import numpy as np
from filehandler import TableIO
from filehandler import DistanceTableIO
from csvhandler import CSVHandler
import random

class Dataset(object):
	'''
	Abstracts numpy.matrix as an undirected graph 
	'''
	def __init__(self, matrix):
		self._matrix = matrix

	def __str__(self): return self._matrix.__str__()
	def tolist(self): self._matrix.tolist()

	def setvalue(self, edge, value):
		(node_a, node_b) = edge
		(row, column) = self._get_matrix_point(node_a, node_b)
		matrix_list = self._matrix.tolist()
		if (row==None): raise ValueError('no such node \'%s\''%node_a)
		if (column==None): raise ValueError('no such node \'%s\''%node_b)
		matrix_list[row][column] = value
		self._matrix = np.matrix(matrix_list) 

	def has_nodes(self, node_a, node_b):
		(row, col) = self._get_matrix_point(node_a, node_b)
		if row == None or col == None: return False
		return True

	def _get_matrix_point(self, node_a, node_b):
		matrix_list = self._matrix.tolist()
		columnlist = matrix_list[0]
		rowlist = [r[0] for r in matrix_list]
		if (not (node_a in rowlist) or not (node_b in columnlist)): return (None, None)
		row, column = rowlist.index(node_a), columnlist.index(node_b)
		return (row, column)

def read_thai():
	thaitext = open('thaitest.txt', 'r')
	raw = thaitext.read()
	thaitext.close()

	print (raw,len(raw))
	hex_per_word = (len(raw)/len(raw.decode('utf-8')))
	hwords=list()
	hword=str()
	for i in range(len(raw)):
		hword+=raw[i]
		if (i%hex_per_word==2):
			#print(hword)
			hwords.append(hword)
			hword=str()
	
	print(hwords, len(hwords))
	return hwords

def create_stub(hwords):
	dist_table=dict()
	for hword in hwords:
		dist_table[hword] = random.randrange(1,4)
	dist_file = DistanceTableIO('thaidictionary.txt')
	dist_file.write_dist_dict(dist_table)
	print (dist_file.get_dist_dict())

def get_freq(hwords):
	freq_table = dict()
	for hword in hwords:
		if (hword in freq_table):
			freq_table[hword]+=1
		else:
			freq_table[hword]=1
	return freq_table

if (__name__=='__main__'):
	# f = open('test.txt', 'r')
	# print(f.read())
	# print((f.read()))
	# tablefile = TableIO('test.txt')
	# data = Dataset(tablefile.get_matrix())
	# print(data)
	# data.setvalue(('a', 'f'), 99)
	# print(data)

	#create_stub_table() ##generate stub table
	dist_table = DistanceTableIO('thaidictionary.txt').get_dist_dict()
	hwords = read_thai()
	freq_table = get_freq(hwords)
	print(freq_table)
	_sum=0
	for hword in freq_table: _sum+=(freq_table[hword]*dist_table[hword])
	print _sum







