# -*- coding: utf-8 -*- 
from qa import *
from classification import *
from rerank import *
import os

qaset=set_qa().items()
log_t=open("table_addcontextprob.txt","w")
def Calculate():
	ls=[]
	for qa in qaset:
		print qa[0]
		table = Query(qa[0])
		flag=0
		for col in table:
			for answer in qa[1]:
				if col[0]==answer.decode('utf-8'):
					col[0]=1
					flag=1
					break
			if col[0]!=1:
				col[0]=-1
			#print >> log_t, col[0],'\t',col[1],'\t',col[2],'\t',col[3]
		if flag==1:
			for col in table:
				print >> log_t, col[0],'\t',col[1],'\t',col[2],'\t',col[3]


if __name__ == '__main__':
	Calculate()