import csv

class CSVHandler(object):
	def __init__(self, filepath):
		self._filedir = filepath

	def __str__(self):
		filestring = str()
		matrix_list = self.get_list()
		for row in matrix_list:
			for elm in row: filestring+='%s\t'%elm
			filestring+='\n'
		return filestring

	def get_list(self):
		matrix_list=[]
		with open(self._filedir, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				row_elements =[]
				for elm in row:
					if (len(elm)!=0): row_elements.append(elm)
				if (len(row_elements)!=0): matrix_list.append(row_elements)
		return matrix_list

	def write_list(self, L):
		with open(self._filedir, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(L)



if (__name__=='__main__'):

	csvopener = CSVHandler("/Users/NatchaS/Desktop/csv_upperkeyboard_coordinates.csv")
	thai_upper_coords = csvopener.get_list()
	for row in thai_upper_coords:
		print ("\n\n\n\t\t\t\t\t\t\t%s %s")%(row[0], row[1])
		print (row[0].decode('utf-8'), row[1])
	print('\n\n\n\n%i'%len(thai_upper_coords))


	# pass
	# filehandler = CSVHandler('csv_upperkeyboard_coordinates.csv')
	# upper= filehandler.get_list()
	# print(type(upper[0]))
	# numbers = [str(i) for i in range(10)]
	# thai_numbers = ['\xe0\xb9\x90','\xe0\xb9\x91','\xe0\xb9\x92','\xe0\xb9\x93','\xe0\xb9\x94','\xe0\xb9\x95','\xe0\xb9\x96','\xe0\xb9\x97','\xe0\xb9\x98','\xe0\xb9\x99']
	# thai_number_table = dict()
	# for nkey in numbers: 
	# 	#print int(nkey)
	# 	thai_number_table[int(nkey)] = thai_numbers[int(nkey)]

	# #for nkey in thai_number_table: print ('%s - %s'%(str(nkey), thai_number_table[nkey]))
	# #print upper[3][0], thai_number_table[int(upper[3][0])]
	# for row in range(len(upper)): 
	# 	if (upper[row][0] in numbers):
	# 		print upper[row][0]
	# 		#upper[row][0] =  99#'\xe0\xb8\x8e'
	# 		print thai_number_table[int(upper[row][0])] 
	# 		#print(thai_number_table[upper[row][0]])
	# 	#print upper[row]

	# for row in upper: print row

	#matlist = filehandler.tolist()
	#print((filehandler, 0))