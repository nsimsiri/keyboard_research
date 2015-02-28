from csvhandler import CSVHandler


point = (28, 753)
points = list()
del_x = 53
del_y = 86
row = 4
col = 12

for r in range(row):
	_rows=list()
	for c in range(col):
		if (not(r==row-1 and (c==0 or c==col-1))):
			_rows.append((point[0]+del_x*c, point[1]+del_y*r))
	points.append(_rows)

#for row in points: print row, len(row)

onelist = []
for row in points: 
	for r in row: onelist.append(r)
#print onelist, len(onelist)

handler = CSVHandler('upperkeyboard.csv')
twolist = []
handlerlist = handler.get_list()
for row in handlerlist:
	for r in row: twolist.append(r)
print twolist, len(twolist)
finallist=[]
if (len(onelist)==len(twolist)):
	for i in range(len(onelist)):
		finallist.append([twolist[i], '%s, %s'%(str(onelist[i][0]), str(onelist[i][1]))])
		#print [twolist[i], onelist[i]]
	

for jk in finallist: print jk

handler.write_list(finallist)
