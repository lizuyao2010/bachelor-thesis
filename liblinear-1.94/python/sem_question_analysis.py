# -*- coding: utf-8 -*-
import urllib2
from read_function import *
def extract_contexts(w,sent):
    contexts=[]
    n=0
    for word in sent:
      if word[12]=='Y':
          verb=word[3]
          n+=1
          A0=''
          A1=''
          for row in sent:
              if row[13+n]=='A0' and (row[5]=='NR' or row[5]=='NN'):
                  A0=row[3]
              if row[13+n]=='A1' and (row[5]=='NR' or row[5]=='NN'):
                  A1=row[3]
          if A0:
              if A0==w[3]:
                pair=('X',verb)
                contexts.append(pair)
                if A1:
              	  triple=('X',verb,A1)
                  contexts.append(triple)
          if A1:
              if A1==w[3]:
                 pair=(verb,'X')
                 contexts.append(pair)
                 if A0:
              	   triple=(A0,verb,'X')
              	   contexts.append(triple)
    return contexts


def question_analysis(question):
   post_data = "sentence="+question
   content=urllib2.urlopen("http://barbar.cs.lth.se:8091/parse",data=post_data).read()
   content=content.split('\n')
   sent=[]
   for row in content:
      table=row.split('\t')
      sent.append(table)
   i = 0
   n=0
   for word in sent:
      if word[12]=='Y':
         n+=1
      if word[3]=='谁':
         word[5]='NN'
         return extract_contexts(word,sent)
      elif word[3]=='什么':
         word[5]='NN'
         return extract_contexts(word,sent)
      elif word[3]=='哪里' or word[1]=='在哪':
         word[5]='NN'
         return extract_contexts(word,sent)
      elif word[3]=='哪一' or word[3]=='哪个' or word[3]=='哪位' or word[3]=='哪家' or word[3]=='哪种' or word[3]=='哪些' or word[1]=='哪':
         for wordj in sent[i+1:]:
            if wordj[5]=='NN':
               return [('X','是'),('X','是',wordj[3])]
         return []
      elif word[3]=='？':
         word[5]='NN'
         word[13+n]='A1'
         return extract_contexts(word,sent)
      else:
         None
      i+=1

   return []


if __name__=='__main__':
   contexts=question_analysis('2000年的资讯科技大会在何地举办？')
   print len(contexts)
   for context in contexts:
    for item in context:
      print item,
    print
