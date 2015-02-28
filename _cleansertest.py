from textanalyzer import TextAnalyzer
from datacleaner import DataCleanser

if __name__ == "__main__":
	# text = 'sample_numbers.txt'
	# analyzer = TextAnalyzer(text, 'csv_upperkeyboard_coordinates.csv', 'csv_lowerkeyboard_coordinates.csv')

	#cleanser = DataCleanser(analyzer.text, analyzer.keychart.get_nodes())

	cleanser = DataCleanser('11		222a		2bbc33', ['a','b','c',u'\u0e50',u'\u0e51',u'\u0e52',' '])
	##replacement test
	for letter in cleanser.rawtext: print letter
	print cleanser.rawtext
	print (cleanser.rawtext, len(cleanser.rawtext))
	print cleanser.cleanse()
	
