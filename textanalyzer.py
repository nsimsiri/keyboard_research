import random
import math
import os
import numpy as np
from charactergraph import CharacterGraph
from keyboardhandler import KeyboardTranslator
from keyboardhandler import OverloadKeyboardTranslator
from datacleaner import DataCleanser
from statistics import KeyTraversalStatistics
class TextAnalyzer(object):
	def __init__(self, upper_keyboard, lower_keyboard):
		keyboard_subtypes = [upper_keyboard, lower_keyboard]
		self.keychart = self.unify_conventional_keyboard(keyboard_subtypes)

	def calculate_paths(self, filepath, find_shortestpath):
		_file = open(filepath, 'r')
		text =  _file.read().decode('utf-8')
		_file.close()
		print("\nRAW TEXT: %s\n"%text)
		cleanser = DataCleanser(text, self.keychart.get_nodes())
		text = cleanser.cleanse()
		return text, self.calculate_traversal_path(text, find_shortestpath)

	def calculate_traversal_path(self, text, find_shortestpath):
		''' find_shortestpath returns ~> r1, r2, such that 
		 (r1) = (shortestpath_value,
		 (r2) = shortestpath : [((a, b), dis) ..])
		'''
		edges = [edge_val[0] for edge_val in self._get_edge(text, self.keychart)]
		shortestpath_value, shortest_path, tables = find_shortestpath(edges, self.keychart)#s.t shortestpath_table = [((a, b), dis) ..]
		#print self.keychart
		return tables

	def _get_edge(self, text, chart): 
		## get consecutive pairs of characters 
		pairs = []
		for i in range(1, len(text)):
			unicodedword_1 = text[i-1]
			unicodedword_2 = text[i]
			if chart.has_node(unicodedword_1) and chart.has_node(unicodedword_2):
				pairs.append(((unicodedword_1, unicodedword_2),chart.get_edge(unicodedword_1, unicodedword_2)))
			else: raise ValueError('TextAnalyzer: _get_edge: chart has no letter -> %s, %s'%(unicodedword_1, unicodedword_2))
		return pairs

	def unify_conventional_keyboard(self, keyboard_subtypes):
		upper_trans = KeyboardTranslator(keyboard_subtypes[0])
		lower_trans = KeyboardTranslator(keyboard_subtypes[1])
		upperkeys, uppertable=upper_trans.get_chart(is_upper_key=True), upper_trans.get_coordinate_table()
		lowerkeys, lowertable =lower_trans.get_chart(), lower_trans.get_coordinate_table()
		return KeyboardTranslator.combine_keyboard(upperkeys, lowerkeys, uppertable, lowertable) 

if __name__ == '__main__':
	text = 'overload_thai_text_2.txt'

	''' REAL-KEYBOARD Unit Test 1 '''
	analyzer = TextAnalyzer('csv_upperkeyboard_coordinates.csv', 'csv_lowerkeyboard_coordinates.csv')
	shiftkey_table = analyzer.calculate_paths(text, KeyboardTranslator.find_shortestpath)
	
	ovanalyzer = TextAnalyzer('csv_upperkeyboard_coordinates.csv', 'csv_lowerkeyboard_coordinates.csv')
	overloadkey_table = ovanalyzer.calculate_paths(text, OverloadKeyboardTranslator.find_shortestpath)

	# print('\n%s\n%i\n'%(shiftkey_table, shiftkey_table.get_distance()))
	# print('\n%s\n%i\n'%(overloadkey_table, overloadkey_table.get_distance()))
	assert (len(overloadkey_table)==len(shiftkey_table))
	stat = KeyTraversalStatistics(overloadkey_table, shiftkey_table)
	print (stat)
	stat.get_overload_frequency_table()
	av_table =  stat.get_average_saved_distance()
	KeyTraversalStatistics.get_total_saved_distance(av_table)
	# Results:
	# print('\n\n')
	# print (OverloadKeyboardTranslator._formulate_pathstring(_key_path))
	# print "Distance: %s pix"%str(_distance)
	# print "Keypress Count: %s"%str(len(_key_path))
	# print (OverloadKeyboardTranslator._formulate_pathstring(ov_key_path))
	# print "Distance %s pix"%str(ov_distance)
	# print "Keypress Count: %s"%str(len(ov_key_path))

class AnalyzerStub:
	''' Unit Testing for TextAnalyzer'''
	def __init__(self, filedir):
		textfile = open(filedir, 'r')
		text = textfile.read()
		textfile.close()
		uni=text.decode("utf-8")
		self.unicode_text = uni
		wordset = dict()
		self.unique_word_list = []
		for word in self.unicode_text:
			if (not(word in wordset)): 
				wordset[word] = True
				self.unique_word_list.append(word)
		self.matrix_list =  self._construct_empty_character_graph()

	def get_matrix_string(self):
		matstring = str()
		for row in self.matrix_list:
			for elm in row:
				if (type(elm)!=unicode): matstring+='%s\t'%str(elm)
				else: matstring+='%s\t'%elm
			matstring+='\n'
		return matstring

	def generate_randomized_matrix(self, bound):
		matrix_list = self.matrix_list
		for row in matrix_list:
			for i in range(len(row)):
				if (row[i]==None):
					randval = random.random()
					row[i]=int(randval*bound)
		self.matrix_list = matrix_list
		return matrix_list

	def generate_randomized_coordinate(self, bound):
		coordinate_table = dict()
		for elm in self.unique_word_list: 
			coordinate_table[elm] = (int(random.random()*bound), int(random.random()*bound))
		return coordinate_table

	def generate_matrix_from_randomized_coordinate(self, bound, chart):
		coordinate_table = self.generate_randomized_coordinate(bound)
		coorList = [(key, coordinate_table[key]) for key in coordinate_table.keys()]
		print coorList
		for i in range(len(coorList)):
			listToCheck = coorList
			(c_key, c_value) = coorList[i]
			for (key, value) in listToCheck:
				if (chart.has_edge(c_key, key)):
					print ("(%s, %s)=>%s"%(c_key.encode('utf-8'), key.encode('utf-8'), str(TextAnalyzer.calculate_traversal_distance(c_value, value))))
					chart.setvalue((c_key, key), int(TextAnalyzer.calculate_traversal_distance(c_value, value)))

		return chart

	def _construct_empty_character_graph(self):
		columns = [-1]+self.unique_word_list
		matrix=[columns]
		for i in range(len(self.unique_word_list)):
			row = [self.unique_word_list[i]]+(i*[None])+[-1]
			row += (len(columns)-len(row))*[None]
			matrix.append(row)
		for row in matrix: 
			if len(columns)!= len(row): return None
		return matrix






















