import os
import numpy as np
from csvhandler import CSVHandler

class CharacterGraph(object):
	'''
	is an Adjacency Matrix 

	flaws: constructor should provide a way to construct CharacterGraph through providing ==>
		(1) nodes 
		(2) arbitrary way of defining edges without the relying through instantiation through another class (for now, KeybaordTranslator)
	'''
	def __init__(self, matrix_list=None):
		self._matrix = np.matrix([])
		if (type(matrix_list)==list):	
			if (len(matrix_list)>0): 
				if (type(matrix_list[0])==list): self._matrix = np.matrix(matrix_list)
				else: self._matrix =np.matrix(CharacterGraph.create_empty_from_uniquelist(matrix_list))

	def __str__(self): 
		matrix_list = self._matrix.tolist()
		matrix_string=str()
		for row in matrix_list:
			for elm in row:
				if (type(elm)==unicode): matrix_string +='%s\t'%str(elm.encode("utf-8"))
				else: matrix_string += '%s\t'%elm
			matrix_string+='\n'
		return matrix_string

	def __add__(self, other):
		new_node_list = self._reduce_node_redundancy(other.get_nodes() + self.get_nodes())
		#print new_node_list
		#new_node_list = other.get_nodes() + self.get_nodes()
		new_graph = CharacterGraph(CharacterGraph.create_empty_from_uniquelist(new_node_list))
		for node_a in new_node_list:
			for node_b in new_node_list:
				if (self.has_edge(node_a, node_b)): new_graph.setvalue((node_a, node_b), self.get_edge(node_a, node_b))
				elif (other.has_edge(node_a, node_b)): new_graph.setvalue((node_a, node_b), other.get_edge(node_a, node_b))
				else: new_graph.setvalue((node_a, node_b), None)
		return new_graph

	def size(self): return len(self._matrix)-1
	def tolist(self): return self._matrix.tolist()
	def replace_nodename(self, node, new_node):
		nodes = self.get_nodes()
		matrixlist = self._matrix.tolist()
		if (self.has_node(node)):
			indexToAlter=0
			for i in range(len(matrixlist[0])):
				if (matrixlist[0][i]==node): 
					matrixlist[0][i]=new_node
					indexToAlter=i
					break
			matrixlist[indexToAlter][0] = new_node
		self._matrix = np.matrix(matrixlist)
			
	def setvalue(self, edge, value):
		(node_a, node_b) = edge
		(row, column) = self._get_matrix_point(node_a, node_b)
		matrix_list = self._matrix.tolist()
		if (row==None): raise ValueError('no such node \'%s\''%node_a)
		if (column==None): raise ValueError('no such node \'%s\''%node_b)
		matrix_list[row][column] = value
		#print(value, type(value))
		self._matrix = np.matrix(matrix_list) 
		#print(self._matrix,0)


	def has_edge(self, node_a, node_b):
		(row, col) = self._get_matrix_point(node_a, node_b)
		if row == None or col == None: return False
		return True

	def has_node(self, node): return node in self.get_nodes()
		
	def get_nodes(self):
		if (len(self._matrix)==0): return [] 
		return self._matrix.tolist()[0][1:] #list[0]=>[-1, node1, node2...] so remove 0 => 1:

	def get_edge(self, node_a, node_b):
		(row, column) = self._get_matrix_point(node_a, node_b)
		matrix_list = self._matrix.tolist()
		if (row==None): raise ValueError('no such node \'%s\''%node_a)
		if (column==None): raise ValueError('no such node \'%s\''%node_b)
		return matrix_list[row][column]

	def _get_matrix_point(self, node_a, node_b):
		matrix_list = self._matrix.tolist()
		if (len(matrix_list)>1):
			columnlist = matrix_list[0]
			rowlist = [r[0] for r in matrix_list]
			if (not (node_a in rowlist) or not (node_b in columnlist)): return (None, None)
			row, column = rowlist.index(node_a), columnlist.index(node_b)
			return (row, column)
		return (None, None)

	def _reduce_node_redundancy(self, nodes):
		unique_nodes = dict()
		for node in nodes:
			if (not(node in unique_nodes)): unique_nodes[node] = True
		#print unique_nodes.keys()
		return unique_nodes.keys() 

	@staticmethod
	def create_empty_from_uniquelist(unique_word_list):
		columns = [0]+unique_word_list
		matrix=[columns]
		for i in range(len(unique_word_list)):
			row = [unique_word_list[i]]+(i*[None])+[0]
			row += (len(columns)-len(row))*[None]
			matrix.append(row)
		for row in matrix: 
			if len(columns)!= len(row): return None
		return matrix


if __name__=='__main__':

	# Unit Testing - 1
	filehandler = CSVHandler('replacetest.csv')

	chart = CharacterGraph(filehandler.get_list())
	print chart
	chart.replace_nodename('e','z')
	print chart
	# node1, node2 = chart.get_nodes()[0], chart.get_nodes()[1]
	# chart.setvalue((node1, node2), 99)
	# print(chart)

	# Unit Testing - 2 - testing __add__() 
	# file_normalthai = CSVHandler('thaiset_normal.csv')
	# file_shiftthai = CSVHandler('thaiset_shift.csv')
	# normalthai_chart = CharacterGraph(file_normalthai.get_list())
	# shiftthai_chart = CharacterGraph(file_shiftthai.get_list())
	# print(normalthai_chart)
	# print(shiftthai_chart)
	# sum_chart = normalthai_chart + shiftthai_chart
	# print(sum_chart)
	# print(sum_chart + CharacterGraph())


















