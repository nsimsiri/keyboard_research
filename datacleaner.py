class DataCleanser(object):

	def __init__(self, text, domainList):
		self.rawtext = text
		self.domain = dict()
		for elm in domainList:
			if (not(elm in self.domain)):
				self.domain[elm] = True

	def cleanse(self):
		replaced_text = self._replace(self.rawtext)
		cleansed_text = self._filter(replaced_text)
		return cleansed_text

	def _replace(self, raw_text):
		''' replace things in string '''
		number_table = {
					'0':'\xe0\xb9\x90',
					'1':'\xe0\xb9\x91',
					'2':'\xe0\xb9\x92',
					'3':'\xe0\xb9\x93',
					'4':'\xe0\xb9\x94',
					'5':'\xe0\xb9\x95',
					'6':'\xe0\xb9\x96',
					'7':'\xe0\xb9\x97',
					'8':'\xe0\xb9\x98',
					'9':'\xe0\xb9\x99'
					}
		for std_num in number_table: 
			number_table[std_num] = number_table[std_num].decode('utf-8')

		spacekey = ' '
		# replacing tabs
		replaced_text = raw_text.replace('\t',spacekey)

		# replacing english numebers to thai numbers
		for std_num in number_table.keys():
			replaced_text = replaced_text.replace(std_num, number_table[std_num])

		return replaced_text

	def _filter(self, replaced_text):
		filtered_string = str()
		space_count=0
		enter_count=0
		print(replaced_text)
		for letter in replaced_text:
			if letter in self.domain:
				if (letter == ' '): space_count+=1
				else: space_count=0
				if (letter == '\n'): enter_count+=1
				else:  enter_count=0
				if (space_count==1): filtered_string += ' '
				if (enter_count==1): filtered_string +='\n'
				elif (space_count==0 and enter_count==0): filtered_string+=letter
		return filtered_string


if (__name__ == '__main__'):
	text = 'ab    \n\n\n\n    \n\n\n\n     c      a    c   d         a \n\n\na\n\n\n\n\n\n\nc'
	cleaner=  DataCleanser(text, ['a', 'b', 'c', ' ', '\n'])
	print (cleaner.cleanse())






