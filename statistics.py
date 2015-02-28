from KeyTraversal import KeyTraversalTable
from KeyTraversal import KeyPathData
from overloadtable import OverloadTable


class KeyTraversalStatistics(object):
	def __init__(self, overloadkey_table, conventionalkey_table):
		self.overloadtable = OverloadTable()
		self.overloadkey_table = overloadkey_table
		self.conventionalkey_table = conventionalkey_table

	def __str__(self):
		statstring = str()
		statstring += 'CONVENTIONAL PATHS: \n%s'%self.conventionalkey_table
		statstring += 'OVERLOAD PATHS: \n%s'%self.overloadkey_table
		print(type('%s'%statstring))
	
		return '%s'%statstring

	def get_overload_distance_keypress(self): return self.overloadkey_table.get_distance(), self. overloadkey_table.get_keypresscount()
	
	def get_conventional_distance_keypress(self): return self.conventionalkey_table.get_distance(), self. conventionalkey_table.get_keypresscount()

	def get_overload_seekcount(self): return self.overloadkey_table.get_seekcount()

	def get_conventional_seekcount(self): return self.conventionalkey_table.get_seekcount()

	def get_overload_frequency_table(self):
		''': Dict(String => Int)'''
		freq_table=dict()
		for edge in self.overloadkey_table.get_edges():
			(from_node, to_node) = edge
			path = self.overloadkey_table.get_keypathdata(edge)
			if (path.is_overloaded() and len(path)>=1):
				pathlist = path.get_path()
				overload_top_key = pathlist[1]  ### second element in path must be -> overloaded top key
				overloaded_key = to_node ### -> overloaded key
				if (self.overloadtable.has_key(overload_top_key) and self.overloadtable.has_overloaded_key(overloaded_key)):
					if (not(to_node in freq_table)): freq_table[to_node] = path.freq()
					else: 
						freq = freq_table[to_node]
						freq_table[to_node] = freq + path.freq()
		'''Debug'''
		for key in freq_table: print('%s : %i\n'%(key, freq_table[key]))
		return freq_table

	def get_average_saved_distance(self): 
		''' Dict(String => Tuple(Int, Int)) '''
		savedist_table = dict()
		for edge in self.overloadkey_table.get_edges():
			(from_node, to_node) = edge
			overload_path = self.overloadkey_table.get_keypathdata(edge)
			conventional_path = self.conventionalkey_table.get_keypathdata(edge)
			if (overload_path.pathdistance()!=conventional_path.pathdistance()):
				print('dif size: (%s,%s)'%(from_node, to_node))
			if (overload_path.is_overloaded()):
				## (from_node, to_node) is overloaded, and must also be in conventional_path
				if (edge in self.conventionalkey_table):
					
					if (not(to_node in savedist_table)):
						savedist_table[to_node] = (float(conventional_path.pathdistance()-overload_path.pathdistance()), overload_path.freq())
					else: 
						(saved_distance, freq) = savedist_table[to_node] 
						saved_distance = saved_distance*freq
						freq += overload_path.freq()
						saved_distance = float((saved_distance+float(conventional_path.pathdistance()-overload_path.pathdistance()))/freq)
						savedist_table[to_node] = (saved_distance, freq)

				else: 
					print "(ERROR)ValueError: no edge found in conventional table: (%s, %s)"%(edge[0], edge[1])
					raise ValueError()

		print('Average Saved Distance Table:\n') 
		for key in savedist_table: print('%s : distance saved: %i, freq: %i \n')%(key, savedist_table[key][0], savedist_table[key][1])
		return savedist_table



	@staticmethod 
	def combine_average_distance_tables(average_distance_tables):
		'''table[String] = Tuple(Int, Int)'''
		combined_av = dict()
		if (len(average_distance_tables)!=0):
			for av_table in average_distance_tables:
				for key in av_table:
					if (not(key in combined_av)):
						combined_av[key] = av_table[key]
					else:
						(c_saved_distance, c_freq) = combined_av[key] # savedist_table[to_node] 
						(saved_distance, freq) = av_table[key]
						total_distance = float(c_saved_distance*c_freq+saved_distance*freq)
						total_freq = c_freq+freq
						combined_av[key] = (float(total_distance/total_freq), total_freq)
		return combined_av
				

	@staticmethod 
	def combine_total_distance_tables(total_distance_tables):
		return KeyTraversalStatistics.combine_frequency_tables(total_distance_tables)

	@staticmethod 
	def combine_frequency_tables(freq_tables):
		'''table[String] = Int'''
		combined_freq = dict()
		if (len(freq_tables)!=0):
			for freq_table in freq_tables:
				for key in freq_table:
					if (not(key in combined_freq)):
						# dun have this key, add this key
						combined_freq[key] = freq_table[key]
					else:
						combined_freq[key] = combined_freq[key]+freq_table[key]
		return combined_freq

	@staticmethod 
	def get_total_saved_distance(savedistance_table):
		totaldist_table=dict()
		for data_key in savedistance_table:
			(saved_distance, freq) = savedistance_table[data_key]
			totaldist_table[data_key] = float(float(saved_distance)*float(freq))

		print('Total Saved Distance:\n')
		for key in totaldist_table:
			print('%s: %s'%(key, totaldist_table[key]))
		return totaldist_table
		
	@staticmethod
	def all_tables_to_string(freq_table, savedist_table, totaldist_table): 
		''': Dict(String => Int)'''
		allstring = str()

		allstring+= ('\nOverload Frequency Table:\n')
		for key in freq_table: allstring += '%s : %f\n'%(key, float(freq_table[key]))

		allstring+=('\nAverage Saved Distance Table:\n')
		for key in savedist_table: allstring+='%s : distance saved: %f, freq: %f \n'%(key, float(savedist_table[key][0]),float(savedist_table[key][1]))

		allstring+=('\nTotal Saved Distance:\n')
		for key in totaldist_table: allstring += ('%s: %s\n'%(key, totaldist_table[key]))

		return allstring.encode('utf-8')


if __name__ == '__main__':
	# freq1 = dict({'a':1, 'b':2})
	# freq2 = dict({'a':5, 'c':3})
	# combfreq=  KeyTraversalStatistics.combine_frequency_table([freq1, freq2])
	# print combfreq

	avtab1=  {'a':(5, 2), 'b':(19, 1)}
	avtab2 = {'a':(12, 4), 'd':(10, 2)}
	print KeyTraversalStatistics.combine_average_distance_table([avtab1, avtab2])

