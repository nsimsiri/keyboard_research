import random
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
		print(hword)
		hwords.append(hword)
		hword=str()
	
#print(hwords, len(hwords))

dist_table=dict()
for hword in hwords:
	dist_table[hword] = random.randrange(1,4)

print (dist_table)