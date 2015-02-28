from textanalyzer import TextAnalyzer
from statistics import KeyTraversalStatistics
from keyboardhandler import KeyboardTranslator
from keyboardhandler import OverloadKeyboardTranslator
from csvhandler import CSVHandler
from time import gmtime, strftime
import os

class Experiment(object):
	def __init__(self):
		self.result_dir = 'Results/'
		self.twitter_dir = 'Twitts/'
		self.news_dir = 'News/'
		self.formal_dir = 'FormalLetters/'

		time_string = strftime("%Y-%m-%d %H:%M:%S")
		self.write_log(time_string)

	def get_data_samples(self):
		samplelist = []

		#samplelist+=['%sN%i.txt'%(self.news_dir, i) for i in range(10)]
		#samplelist+=['%sT%i.txt'%(self.twitter_dir, i) for i in range(100)]
		samplelist+=['%sF%i.txt'%(self.formal_dir, i) for i in range(10)]

		#samplelist += ['overload_thai_text_3.txt','overload_thai_text_5.txt']
		return samplelist

	def run(self):
		samples = self.get_data_samples()
		for sample in samples: print sample
		self.perform_analysis(samples)

	def perform_analysis(self, dataset_files):
		
		#dataset_files = ['sample_1.txt']#, 'sample_2.txt']#, 'sample_3.txt']

		''' REAL-KEYBOARD Unit Test 1 '''
		analyzer = TextAnalyzer('csv_upperkeyboard_coordinates.csv', 'csv_lowerkeyboard_coordinates.csv')
		ovanalyzer = TextAnalyzer('csv_upperkeyboard_coordinates.csv', 'csv_lowerkeyboard_coordinates.csv')

		overload_total_distance=0
		overload_total_keypresscount=0
		conventional_total_distance=0
		conventional_total_keypresscount=0

		overload_total_seekcount = 0
		conventional_total_seekcount = 0

		frequency_tables=[]
		average_tables=[]
		total_tables=[]

		total_filesize=0

		for aText in dataset_files:

			the_text, shiftkey_table = analyzer.calculate_paths(aText, KeyboardTranslator.find_shortestpath)
			the_text2, overloadkey_table = ovanalyzer.calculate_paths(aText, OverloadKeyboardTranslator.find_shortestpath)

			filesize=0

			print "ClEANSED TEXT: %s\n"%the_text
			print(type(the_text))
			cleantext=the_text
			filesize+=len(cleantext)
			print len(cleantext)

			assert (len(overloadkey_table)==len(shiftkey_table))

			stat = KeyTraversalStatistics(overloadkey_table, shiftkey_table)
			print (stat)

			## get analyzed tables
			# (1) distance, keypress count, seek distant
			overload_distance, overload_keypresscount = stat.get_overload_distance_keypress()
			conventional_distance, conventional_keypresscount = stat.get_conventional_distance_keypress()
			conventional_seekcount = stat.get_conventional_seekcount()
			overload_seekcount = stat.get_overload_seekcount()

			# (2)
			freq_table = stat.get_overload_frequency_table()
			# (3) 
			av_table =  stat.get_average_saved_distance()
			# (3)
			tot_table = KeyTraversalStatistics.get_total_saved_distance(av_table)
			alltable_string = KeyTraversalStatistics.all_tables_to_string(freq_table, av_table, tot_table)

			self.write_log(cleantext.encode('utf-8'))
			self.write_log("SIZE: %i"%filesize)
			self.write_log(stat)
			self.write_log(alltable_string)
			self.write_log('OVERLOAD DIST: %i, OVERLOAD KEYPRESS: %s\n, CONVENTIONAL DIST: %i, CONVENTIONAL KEYPRESS: %i'%(overload_distance, overload_keypresscount, conventional_distance, conventional_keypresscount))
			self.write_log('OVERLOAD SEEK: %i, CONVENTIONAL SEEK %i'%(overload_seekcount, conventional_seekcount))

			### Accumulating Total ###
			# (1)
			total_filesize+=filesize
			overload_total_distance+= overload_distance
			overload_total_keypresscount+= overload_keypresscount
			conventional_total_distance += conventional_distance
			conventional_total_keypresscount += conventional_keypresscount

			overload_total_seekcount += overload_seekcount
			conventional_total_seekcount += conventional_seekcount
			#(2)
			frequency_tables.append(freq_table)
			#(3)
			average_tables.append(av_table)
			#(4)
			total_tables.append(tot_table)

		comb_string = "TOTAL SIZE: %i\n"%total_filesize
		comb_string += ('OVERLOAD DIST: %i\nOVERLOAD KEYPRESS: %s\nCONVENTIONAL DIST: %i\nCONVENTIONAL KEYPRESS: %i\n'%(overload_total_distance, overload_total_keypresscount, conventional_total_distance, conventional_total_keypresscount))
		comb_string += ('OVERLOAD SEEK: %i\nCONVENTIONAL SEEK: %i\n'%(overload_total_seekcount, conventional_total_seekcount))
		## Finishing all data - combine them
		comb_freq = KeyTraversalStatistics.combine_frequency_tables(frequency_tables)
		comb_av = KeyTraversalStatistics.combine_average_distance_tables(average_tables)
		comb_total = KeyTraversalStatistics.combine_total_distance_tables(total_tables)
		print ('comb_freq', comb_freq)
		print ('comb_av', comb_av)
		print ('comb_total', comb_total)
		# 3 above combined
		comb_string += KeyTraversalStatistics.all_tables_to_string(comb_freq, comb_av, comb_total)

		self.write_report(comb_string)



	def write_csv(self, data_table, filename):
		if (type(data_table)==dict):
			datalist2d = []
			for key in data_table:
				datarow= [key]
				for elm in data_tabe[key]:
					datarow.append(elm)
				dtalist2d.append(datarow) ## [[key, elm1, elm2], [key2, elm1, elm2]]
			csvManager = CSVHandler(filename)
			csvManger.write_list(datalist2d)
		else: print("cannot write tables to csv file")

	def write_report(self, all_table_string):
		reportstring=str()
		time_string = strftime("%Y-%m-%d %H:%M:%S")
		reportstring = 'Accumulated Data Report\n%s\n'%time_string
		reportstring += all_table_string
		reportdir = self.result_dir+'Report.txt'
		if (not os.path.exists(reportdir)):
			reportfile = open(reportdir, 'w')
			reportfile.close()
		reportfile = open(reportdir, 'w')
		reportfile.write(reportstring)
		reportfile.close()

	def write_log(self, logdata):
		logdata = '%s\n'%logdata
		logdir= self.result_dir+'Log.txt'
	 	if (not os.path.exists(logdir)):
	 		logfile = open(logdir, 'w')
	 		logfile.close()
	 	logfile = open(logdir, 'a')
	 	print(logdata)#, type(logdata))
	 	logfile.write(logdata)
	 	logfile.close()


if __name__=='__main__':
	exp = Experiment()
	exp.run()

	