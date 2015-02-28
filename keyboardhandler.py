import csv
import numpy as np
from charactergraph import CharacterGraph
from csvhandler import CSVHandler
import math
from overloadtable import OverloadTable
from statistics import KeyTraversalStatistics
from KeyTraversal import KeyTraversalTable

class KeyboardTranslator(object):
	'''
	 Translates data related to keyboard to a graph.
	 input as textfile consisting of rows of ['thaikey', '(x, y)']
	 '''
	def __init__(self, filedir):
		tablefile = CSVHandler(filedir)
		coordlist = tablefile.get_list()
		self._coord_table = self._parse_key_value(coordlist)
		self._letters = self._coord_table.keys()
		#print(self._coord_table)

	def get_chart(self, is_upper_key=False):
		## table must be somedict[word] = (x, y)
		coorList = [(key, self._coord_table[key]) for key in self._coord_table.keys()]
		chart = CharacterGraph(self._letters) ## empty graph which nodes consists of letters 
		lower_shift = 'sl'.decode('utf-8')
		upper_shift = 'sr'.decode('utf-8')
		#print coorList
		for i in range(len(coorList)):
			listToCheck = coorList
			(c_key, c_value) = coorList[i]
			for (key, value) in listToCheck:
				if (chart.has_edge(c_key, key)):
					#print ("(%s, %s)=>%s"%(c_key.encode('utf-8'), key.encode('utf-8'), str(KeyboardTranslator.calculate_traversal_distance(c_value, value))))
					chart.setvalue((c_key, key), int(KeyboardTranslator.calculate_traversal_distance(c_value, value)))
					if (is_upper_key ): 
						## if keyboard is all upper, but they must still be able to go through shifts
						if ((c_key != lower_shift and c_key != upper_shift) and (key != lower_shift and key != upper_shift)):
							chart.setvalue((c_key, key), None) 
		return chart
	def get_coordinate_table(self): return self._coord_table

	def _parse_key_value(self, coord_list):
		## translates what's inside csv to dictionary[key] = value s.t. value = (x, y)
		coord_table = dict()
		for row in coord_list:
			#key, value = row[0].strip().decode('utf-8'), self._parse_value_to_tuple(row[1])
			key, value = row[0].decode('utf-8'), self._parse_value_to_tuple(row[1])
			coord_table[key] = value
		return coord_table

	def _parse_value_to_tuple(self, value):
		parsed_val = value.split(',')
		x, y = float(parsed_val[0]), float(parsed_val[1])
		return tuple((x,y))

	@staticmethod
	def combine_keyboard(upperkeys, lowerkeys, uppertable, lowertable):
		combined_chart = upperkeys + lowerkeys
		# print(combined_chart)
		# print('upper=> %s'%uppertable)
		# print('lower=> %s'%lowertable)
		nodes = combined_chart.get_nodes()
		lower_shift = 'sl'.decode('utf-8')
		upper_shift = 'sr'.decode('utf-8')
		for letter_a in nodes:
			for letter_b in nodes:
				if (combined_chart.has_edge(letter_a, letter_b) and combined_chart.has_node(lower_shift) and combined_chart.has_node(upper_shift)):
					if (combined_chart.get_edge(letter_a, letter_b)==None): 
						## combinig
						if (upperkeys.has_node(letter_a) and lowerkeys.has_node(letter_b)):
							point_a, point_b = uppertable[letter_a], lowertable[letter_b] 
							combined_chart.setvalue((letter_a, letter_b), int(KeyboardTranslator.calculate_traversal_distance(point_a, point_b)))
				else: raise ValueError ('@KeyboardTranslator: combined keyboard has no node.')		
		#path_chart = 
		combined_chart.replace_nodename('enter', '\n') # *Numbers or csv cannot input a '\n' and is noted by 'enter', hence must modify
		return combined_chart
	@staticmethod
	def find_shortestpath(consecutive_letter_pairs, chart):
		edges = consecutive_letter_pairs
		nodes = chart.get_nodes()
		path = [] ## stores Tuple(Tuple(String, String), Int)
		pathstring = str()
		left_shift = 'sl'.decode('utf-8')
		right_shift = 'sr'.decode('utf-8')
		shiftkey_table = KeyTraversalTable()

		#print("\n\n")
		for edge in edges: 
			letter_a, letter_b = edge[0], edge[1]
			#print 'edge = (%s, %s)'%(letter_a, letter_b)
			if (chart.has_edge(letter_a, letter_b) and chart.has_node(left_shift) and chart.has_node(right_shift)):
				if (chart.get_edge(letter_a, letter_b) == None):
					#print ("\nCASE: (%s, %s)"%(letter_a, letter_b))
					val_thru_shift_left = int(chart.get_edge(letter_a, left_shift)) + int(chart.get_edge(left_shift, letter_b))
					val_thru_shift_right = int(chart.get_edge(letter_a, right_shift)) + int(chart.get_edge(right_shift, letter_b))
					if (val_thru_shift_right<val_thru_shift_left): 
						a_path = [((letter_a, right_shift), int(chart.get_edge(letter_a, right_shift)))]
						a_path += [((right_shift, letter_b), int(chart.get_edge(right_shift, letter_b)))]

						path.append(a_path[0])
						path.append(a_path[1])


						shiftkey_table.append(edge,a_path)		
					else:
						a_path2 = [((letter_a, left_shift), int(chart.get_edge(letter_a, left_shift)))]
						a_path2 += [((left_shift, letter_b), int(chart.get_edge(left_shift, letter_b)))]

						path.append(a_path2[0])
						path.append(a_path2[1])


						shiftkey_table.append(edge,a_path2)
						
				else:
					non_shift_path = [(edge, chart.get_edge(letter_a, letter_b))]
					path += non_shift_path
					shiftkey_table.append(edge,non_shift_path)
			else: raise ValueError('@KeyboardTranslator: shortest-path: element in text not in chart.')
		for index in range(len(path)): 
			#print path[index] 
			((letter_a, letter_b), dist_val) = path[index]
			if (index==0): pathstring += '%s = (%s) => %s' %(letter_a, dist_val, letter_b)
			else: pathstring += ' = (%s) => %s'%(dist_val, letter_b)
		#print KeyboardTranslator.find_shortestpath_matrix(chart) ## shortest path in matrix form
		#print pathstring

		return sum([int(path_value[1]) for path_value in path]), path, shiftkey_table

	@staticmethod
	def find_shortestpath_matrix(chart):
		nodes = chart.get_nodes()
		left_shift = 'sl'.decode('utf-8')
		right_shift = 'sr'.decode('utf-8')
		for letter_a in nodes:
			for letter_b in nodes:
				if (chart.has_edge(letter_a, letter_b) and chart.has_node(left_shift) and chart.has_node(right_shift)):
					if (chart.get_edge(letter_a, letter_b) == None):
						ls_val = int(chart.get_edge(letter_a, left_shift)) + int(chart.get_edge(left_shift, letter_b))
						rs_val = int(chart.get_edge(letter_a, right_shift)) + int(chart.get_edge(right_shift, letter_b))

						if (rs_val < ls_val):
							chart.setvalue((letter_a, letter_b), rs_val)
						else:
							chart.setvalue((letter_a, letter_b), ls_val)
				else: raise ValueError('@KeyboardTranslator: shortest-path: element in text not in chart.')
		return chart

	@staticmethod
	def calculate_traversal_distance(point_a, point_b):
		Ax, Ay = point_a[0], point_a[1]
		Bx, By = point_b[0], point_b[1]
		return math.sqrt(math.pow(abs(Ax-Bx), 2)+math.pow(abs(Ay-By),2))
	
	# @staticmethod
	# def shiftify(combined_chart):
	# 	#print("\n\n")
	# 	nodes = combined_chart.get_nodes()
	# 	shift = 'shift'.decode('utf-8')
	# 	for letter_a in nodes:
	# 		for letter_b in nodes:
	# 			if (combined_chart.has_edge(letter_a, letter_b) and combined_chart.has_node(shift)):
	# 				if (combined_chart.get_edge(letter_a, letter_b)==None): 
	# 					letter_a_to_shift = combined_chart.get_edge(letter_a, shift)
	# 					shift_to_letter_b = combined_chart.get_edge(shift, letter_b)
	# 					a_shift_b = float(letter_a_to_shift) + float(shift_to_letter_b)##=> elements of graph is a unicode u'n'
	# 					#print((letter_a, letter_b), a_shift_b)
	# 					combined_chart.setvalue((letter_a, letter_b), a_shift_b)
	# 	return combined_chart  

class OverloadKeyboardTranslator(KeyboardTranslator):
	def __init__(self, filedir):
		KeyboardHandler.__init__(self, filedir)

	@staticmethod
	def find_shortestpath(consecutive_letter_pairs, chart, overload_enable=True):
		_OVERLOAD_FLAG = False
		previouslyOverloadedLetter = None
		edges = consecutive_letter_pairs
		nodes = chart.get_nodes()
		path = [] ## stores Tuple(Tuple(uString, uString), Int)
		left_shift = 'sl'.decode('utf-8')
		right_shift = 'sr'.decode('utf-8')

		## Overload part
		overloadTable = OverloadTable()
		## stats!
		overloadkey_table = KeyTraversalTable()

		for edge in edges: 
			letter_a, letter_b = edge[0], edge[1]
			always_letter_a = letter_a
			#print("new round\n\n")
			if (_OVERLOAD_FLAG): 
				## because you're not going from this edge's letter_a, you're going from the overloaded key you pressed
				letter_a = previouslyOverloadedLetter
				#print('preivious assigned: %s'%letter_a)
				_OVERLOAD_FLAG = False
			#print 'edge = (%s, %s)'%(letter_a, letter_b)
			if (chart.has_edge(letter_a, letter_b) and chart.has_node(left_shift) and chart.has_node(right_shift)):
				#print('letter_a used: %s\n'%letter_a)
				if (chart.get_edge(letter_a, letter_b) == None):
					''' find shortest path here
						note* a Path in this scope is list of Tuple(Tuple(uString, uString), Int)
					'''
					
					#print ("\nCASE: (%s, %s)"%(letter_a, letter_b))
					# SHIFT
					val_thru_shift_left = int(chart.get_edge(letter_a, left_shift)) + int(chart.get_edge(left_shift, letter_b))
					val_thru_shift_right = int(chart.get_edge(letter_a, right_shift)) + int(chart.get_edge(right_shift, letter_b))
					_UPPERBOUND = val_thru_shift_right + val_thru_shift_left

					shift_path = []
					shift_val =  _UPPERBOUND ## since its an upper bound for either right or left
					if (val_thru_shift_right<val_thru_shift_left): 
						shift_path.append(((letter_a, right_shift), int(chart.get_edge(letter_a, right_shift))))
						shift_path.append(((right_shift, letter_b), int(chart.get_edge(right_shift, letter_b))))
						shift_val = val_thru_shift_right	
					else:
						shift_path.append(((letter_a, left_shift), int(chart.get_edge(letter_a, left_shift))))
						shift_path.append(((left_shift, letter_b), int(chart.get_edge(left_shift, letter_b))))
						shift_val = val_thru_shift_left

					# OVERLOAD
					overload_pair= tuple()
					overload_val = _UPPERBOUND ## since its an upper bound for either shifts
					overload_path = []
					if (overloadTable.has_overloaded_key(letter_b)):
						## check and find minimum value of all possible keys the overloaded key (letter_b) belongs to
						possibleHeadKeys = overloadTable.get_keys_from_overloaded_key(letter_b)
						minKey = (int(chart.get_edge(letter_a, possibleHeadKeys[0])), possibleHeadKeys[0]) ## (Int, uString)
						for possibleHeadKey in possibleHeadKeys:
							minVal = minKey[0]
							newKeyVal = int(chart.get_edge(letter_a, possibleHeadKey))
							if (newKeyVal<minVal):
								minKey = (newKeyVal, possibleHeadKey)
						overload_top_key, overload_min_val = minKey[1], minKey[0]
						overload_val = overload_min_val
						overload_pair = (letter_a, overload_top_key)
						overload_path = [(overload_pair, overload_val)]

					'''Debug 1'''	
					# if (len(overload_pair)==0): overload_pair += (None, None)	
					# for ((a, b), ival) in overload_path + shift_path: print ('(%s, %s) -> %s'%(a, b, ival)) 

					'''Debug 1 end'''
					## 
					
					if (shift_val<overload_val and ((not overload_enable) or len(overload_path)==0)):
						## ---- SHIFT
						path += shift_path
					else:
						## ---- OVERLOADED
						(cur_key, cur_overloaded_top_key) = overload_pair

						## cache overloaded top key as previous key press since they came from this overload key keypress
						_OVERLOAD_FLAG = True
						previouslyOverloadedLetter = cur_overloaded_top_key 

						# cur_key -> cur_overloaded_top_key -> [overload key_1, overload key_2...]
						overload_list = overloadTable.get_overloadedkeys(cur_overloaded_top_key)
						#for _over in overload_list: print('overloading: %s' %_over)
						overload_stack_value=overload_val ## first loop is the distance from letter_a -> overloaded top key, then the rest will be 0 since it is overloaded
						for overload_key in overload_list:
							overload_path.append(((cur_overloaded_top_key, overload_key), 0))
							if (overload_key == letter_b): 
								break
						path += overload_path

					'''
					Stats: this function has both shiftpath and overloadpath. Will only get to use shiftpath 

					'''

					# print overload_path
					# print shift_path

					if (len(overload_path)!=0):
						## if letter is not in overloaded list, must use shiftpath
						overloadkey_table.append((always_letter_a, letter_b), overload_path, isOverload=True) #overloadkey_table 1 --> case key is overloaded
					else: 
						## case where no overload path available
						overloadkey_table.append((always_letter_a, letter_b), shift_path) #overloadkey_table 2 --> case no overloading, but shifting because no overload available

					#shiftkey_table.append((letter_a, letter_b), shift_path)

				else:
					#print('special path %s'%letter_a)
					dist = chart.get_edge(letter_a, letter_b)
					path_with_no_comparison = [((letter_a, letter_b), dist)]
					overloadkey_table.append(edge, path_with_no_comparison) #overloadkey_table 3 -> case direct pathway 

					path += path_with_no_comparison
			else: raise ValueError('@OverloadKeyboardTranslator: shortest-path: element in text not in chart.')
		

		''' Finished '''
		
		pathstring = OverloadKeyboardTranslator._formulate_pathstring(path)
		#print pathstring

		return sum([int(path_value[1]) for path_value in path]), path, overloadkey_table

	@staticmethod 
	def _formulate_pathstring(path):
		pathstring = str()
		for index in range(len(path)):  
			((letter_a, letter_b), dist_val) = path[index]
			if (index==0): pathstring += '%s = (%s) => %s' %(letter_a, dist_val, letter_b)
			else: pathstring += ' = (%s) => %s'%(dist_val, letter_b)
		return pathstring

if (__name__=='__main__'):
	# kb_trans = KeyboardTranslator('thai_lower.csv')
	# print(kb_trans.get_chart())

	#Unit Testing - 3 - Testing __add__() with keyboardhandler
	graph_1 = KeyboardTranslator('thai_upper.csv').get_chart()
	graph_2 = KeyboardTranslator('thai_lower.csv').get_chart()

	# print(graph_1)
	# print(graph_2)

	print type(graph_1.get_edge(graph_1.get_nodes()[0], graph_1.get_nodes()[1]))
