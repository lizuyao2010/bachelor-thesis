import operator
from math import *

def rerank(y,x,p_vals,prob):
	originrank=0
	nowrank=0
	newrank=[]
	originranks=[]
	newranks=[]
	i=0
	flag=0	
	while i < len(y):
		if y[i]==1 and flag==0:
			originrank=i+1
			flag=1
			print "originrank",originrank
		a=p_vals[i][0]
		newrank.append([y[i],x[i][1],x[i][1]*pow(prob[i],0.5)])
		i+=1
	newrank=sorted(newrank,key=operator.itemgetter(2),reverse=True)
	i=0
	while i<len(newrank):
		if newrank[i][0]==1:
			nowrank=i+1
			print "nowrank",nowrank
			break
		i+=1
	return nowrank,originrank

if __name__ == '__main__':
	delta=rerank()
	print delta
	#print delta
