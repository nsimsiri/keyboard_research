import os
import numpy as np


class TableIO(object):
	'''
	Does I/O on alphabet matrices - translate file <=> numpy.matrix 
	each file line format '[d_1]\t[d_2]\t...[d_n]\t\n'
	'''
	def __init__(self, filedir):
		self._tabledir = filedir
		if (not os.path.exists(self._tabledir)):
			temp_file = open(self._tabledir, 'w')
			temp_file.close()
		
	def __str__(self): 
		temp_file = open(self._tabledir, 'r')
		table = temp_file.read()
		temp_file.close()
		return table

	def get_matrix(self):
		temp_file = open(self._tabledir, 'r')
		table_arr = []
		for line in temp_file: 
			table_arr.append([l.split('\n')[0] for l in line.split('\t') if (len(l.split('\n')[0])!=0)])
		temp_file.close()
		return np.matrix(table_arr)
	
	def write_matrix(self, matrix):
		matrix_arr = matrix.tolist()
		matrix_string = str()
		for arr in matrix_arr:
			for elm in arr:
				matrix_string += '%s\t'%str(elm)
			matrix_string+='\n'
		table = open(self._tabledir, 'w')
		table.write(matrix_string)
		table.close()
		return matrix_string

class DistanceTableIO(object):
	'''
	Does I/O on distance file, translate file <=> dictonary
	'''
	def __init__(self, filedir):
		self._tabledir=filedir
		if (not os.path.exists(self._tabledir)):
			temp_file = open(self._tabledir, 'w')
			temp_file.close()

	def __str__(self): 
		temp_file = open(self._tabledir, 'r')
		table = temp_file.read()
		temp_file.close()
		return table

	def get_dist_dict(self):
		table = open(self._tabledir, 'r')
		dist_dict=dict()
		for line in table:
			row = (line.split('\n')[0]).split('\t')
			if (len(row)==2):
				key, value = row[0], row[1]
				dist_dict[key] = int(value)
		return dist_dict

	def write_dist_dict(self, dist_dict):
		table_string = str()
		for key in dist_dict.keys():
			table_string += '%s\t%s\n'%(key, dist_dict[key])
		table = open(self._tabledir, 'w')
		table.write(table_string)
		table.close()
		

if (__name__=='__main__'):
	table = TableIO('/Users/NatchaS/Documents/workspace/research_b/test.txt')
	table2 = TableIO('/Users/NatchaS/Documents/workspace/research_b/test2.txt')

	#print(table)
	print table.get_table()
	#mat = np.matrix([[1,2],[3,4]])
	#print (table2.write_table(mat), 0)

	# distances = DistanceTableIO('/Users/NatchaS/Documents/workspace/research_b/dist_table.txt')
	# dists = dict({'a':1, 'b':2, 'c':3})
	# print distances.get_dist_dict()
	#print distances.write_dist_dict(dists)	






