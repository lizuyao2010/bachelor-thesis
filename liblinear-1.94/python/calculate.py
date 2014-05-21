# -*- coding: utf-8 -*- 
from qa import *
from classification import *
from rerank import *
import os
from liblinearutil import *

def loadCluster():
	file1=open('map','r')
	maps={}
	paths={}
	for line in file1:
		line=line.strip().split()
		key=line[0].strip()
		value=line[1].strip()
		maps[key]=value
	file1.close()
	file2=open('paths','r')
	for line in file2:
		line=line.strip().split()
		key=line[0].strip()
		if not paths.has_key(key):
			paths[key]=[]
		value=line[1].strip()
		paths[key].append(value)
	file2.close()
	return maps,paths

def Calculate():
	qaset=set_qa().items()
	model=load_model('table1.txt.model')
	oldranks=[]
	newranks=[]
	maps,paths=loadCluster()
	n=1
	for qa in qaset:
		print n,qa[0]
		table = Query(qa[0],maps,paths)
		y=[]
		x=[]
		prob=[]
		for row in table:
			flag=-1
			for answer in qa[1]:
				if row[0].strip()==answer.decode('utf-8'):
					y.append(1)
					flag=1
					break
			if flag==-1:
				y.append(-1)
			x.append(row[1])
			prob.append(row[2])

		if y and x:
			p_labs,p_acc,p_vals=predict(y,x,model,'-b 1')
			new,old=rerank(y,x,p_vals,prob)
			if new and old:
			   newranks.append(new)
			   oldranks.append(old)
		n+=1

	oldranks=sorted(oldranks)
	newranks=sorted(newranks)	
	print "old: ",oldranks[len(oldranks)/2]
	print "new: ",newranks[len(newranks)/2]


if __name__ == '__main__':
	'''
	maps,paths=loadCluster()
	print maps['逃到'],paths['000000011']
	'''
	Calculate()