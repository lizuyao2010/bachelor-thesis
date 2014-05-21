# -*- coding: utf-8 -*-
import urllib2
from read_function import *
def extract_contexts(word,sent):
    contexts=[]
    N2Xs=dealwithchildren(word,sent)
    if N2Xs:
      contexts+=N2Xs
    X2P,triplelist=dealwithparent(word,sent)
    #X2P=dealwithparent(word,sent)
    #contexts.append(X2P)
    if triplelist:
      contexts+=triplelist
    prevN2X=()
    if N2Xs:
        for N2X in N2Xs:
            if N2X and prevN2X:
                N2XN2X = (N2X[0],N2X[1],N2X[2],prevN2X[0],prevN2X[1],prevN2X[2])
                if N2XN2X:
                  contexts.append(N2XN2X)
            if N2X and X2P:
                N2X2P = (N2X[0],N2X[1],N2X[2],X2P[0],X2P[1],X2P[2])
                if N2X2P:
                  contexts.append(N2X2P)
            prevN2X = N2X
    triplelist=dealwithgrandchildren(word,sent)
    if triplelist:
      contexts+=triplelist
    #print contexts
    return contexts


def question_analysis(question):
   post_data = "sentence="+question
   content=urllib2.urlopen("http://barbar.cs.lth.se:8091/parse",data=post_data).read()
   content=content.split('\n')
   sent=[]
   for row in content:
      table=row.split('\t')
      ID = table[0]
      PLemma = table[3]
      PPOS = table[5]
      PHead = table[9]
      PDeprel = table[11]
      sent.append([ID,PLemma,PPOS,PHead,PDeprel])
   i = 0
   for word in sent:
      if word[1]=='谁':
         word[2]='NN'
         return extract_contexts(word,sent)
      elif word[1]=='什么':
         word[2]='NN'
         return extract_contexts(word,sent)
      elif word[1]=='哪里' or word[1]=='在哪':
         word[2]='NN'
         return extract_contexts(word,sent)
      elif word[1]=='哪一' or word[1]=='哪个' or word[1]=='哪位' or word[1]=='哪家' or word[1]=='哪种' or word[1]=='哪些' or word[1]=='哪':
         for wordj in sent[i+1:]:
            if wordj[2]=='NN':
               return [('X','是','SBJ'),('X','是','SBJ',wordj[1],'是','PRD')]
         return []
      elif word[1]=='？':
         word[2]='NN'
         word[4]='PRD'
         return extract_contexts(word,sent)
      else:
         None
      i+=1

   return []


if __name__=='__main__':
   contexts=question_analysis('世界上人口最多的国家是？')
   print len(contexts)
   for context in contexts:
    for item in context:
      print item,
    print
