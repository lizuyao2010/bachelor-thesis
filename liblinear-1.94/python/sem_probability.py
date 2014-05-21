# -*- coding: utf-8 -*- 
from read_triple import *
from sem_question_analysis import *
from cluster import *

d1= returndict1("sem_triple1.txt")
d2 = returndict2("sem_triple2.txt")
allFrequency = sum(d2.values())
def inContext(w,y):
	if w=='all':
		if d2.has_key(y):
			return d2[y]
		else:
			return 0
	elif y=='all':
		if d1.has_key(w):
			return sum(d1[w].values())
		else:
			return 0
	else:
		if d1.has_key(w):
			if d1[w].has_key(y):
				return d1[w][y]
			else:
				#print "d1 has no key",'('+y[0],y[1],y[2]+')'
				return 0
		else:
			#print "d1 has no key",w
			return 0

def probability(w,y):
	numerator = inContext(w,y)
	denominator = allFrequency
	return float(numerator)/denominator

def probability_wordInContext_givenWord(w,y):
	return float(inContext(w,y)+probability("all",y))/(inContext(w,"all")+1)

def uniform_probability_cluster_givenWord(w,c):
	if w in c:
		return 1.0/sizeof(clusters(w))
	else:
		return 0

def probability_cluster_givenWord(w,c):
	numerator=0
	for word in similar_set(w,n=50):
		numerator += sim(w,word)*uniform_probability_cluster_givenWord(word,c)
	denominator=0
	for cluster in clusters(w):
		for word in similar_set(w,n=50):
			denominator += sim(w,word)*uniform_probability_cluster_givenWord(word,cluster)
	if denominator>0:
		return float(numerator)/denominator
	else:
		print "Error:denominator equals 0"

def probability_cluster_givenWordAndWordContext(w,c,Yw):
	numerator=0
	for word in similar_set(w,n=50):
		if inContext(word,Yw)>0:
			numerator += sim(w,word)*uniform_probability_cluster_givenWord(word,c)
	denominator=0
	for cluster in clusters(w):
		for word in similar_set(w,n=50):
			if inContext(word,Yw)>0:
				denominator += sim(w,word)*uniform_probability_cluster_givenWord(word,cluster)
	if denominator>0:
		return float(numerator)/denominator
	else:
		print "Error:denominator equals 0"

def probability_clusterInContext_givenCluster(c,y):
	numerator=0
	for word in c:
		numerator += inContext(word,y)#+probability("all",y)
	denominator=0
	for word in c:
		denominator += inContext(word,"all")#+1

	#if denominator>0:
	return float(numerator+probability("all",y))/(denominator+1)
	#else:
		#print "Error:denominator equals 0"

def probability_wordInQuestionContexts_givenWord(w,Tq,all_clusters):
	sum=0
	for c in all_clusters:
		factor=1
		for Yq in Tq:
			factor*=probability_clusterInContext_givenCluster(c,Yq)
		sum += probability_cluster_givenWord(w,c)*factor
	return sum

def probability_cluster_givenWordAndWordContexts(w,c,Tw):
	factor=1
	for Yw in Tw:
		factor*=probability_cluster_givenWordAndWordContext(w,c,Yw)/probability_cluster_givenWord(w,c)
	return factor*probability_cluster_givenWord(w,c)
	
def probability_wordInQuestionContexts_givenWordAndWordContexts(w,Tq,Tw):
	sum = 0
	for c in all_clusters:
		factor=1
		for Yq in Tq:
			factor*=probability_clusterInContext_givenCluster(c,Yq)
		sum+=probability_cluster_givenWordAndWordContexts(w,c,Tw)*factor
	return sum

if __name__ == '__main__':
	'''
	p = probability_wordInContext_givenWord('中国',('X','在','OBJ'))*probability_wordInContext_givenWord('中国',('X','在','OBJ','首都','在','SBJ'))
	print p
	p = probability_wordInContext_givenWord('铁路',('X','在','OBJ'))*probability_wordInContext_givenWord('铁路',('X','在','OBJ','首都','在','SBJ'))
	print p
	p = probability_wordInContext_givenWord('北京',('X','在','OBJ'))*probability_wordInContext_givenWord('北京',('X','在','OBJ','首都','在','SBJ'))
	print p
	'''
	contexts=question_analysis('中国的首都是哪里？')
	prob=1
	for y in contexts:
		prob*=probability_clusterInContext_givenCluster(['赫鲁晓夫'],y)
	print prob
	#print d1
	'''
	prob=1
	for y in contexts:
		prob*=probability_wordInContext_givenWord('美国',y)
	print prob
	prob=1
	for y in contexts:
		prob*=probability_wordInContext_givenWord('台湾',y)
	print prob
	prob=1
	for y in contexts:
		prob*=probability_wordInContext_givenWord('总统',y)
	print prob
	'''