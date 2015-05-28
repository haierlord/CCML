import copy

def plus(dic1, dic2):
	dic3 = copy.copy(dic1)
	for t in dic2:
		dic3[t] += dic2[t]
	return dic3
	
	
dic1 = {1:2,2:3}
dic2 = {1:5,2:10}
dic3 = plus(dic1, dic2)
print dic3
print dic2
print dic1