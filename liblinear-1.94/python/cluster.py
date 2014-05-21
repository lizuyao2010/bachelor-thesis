# -*- coding: utf-8 -*- 
def cluster(word):
   mapfile='./map'
   paths='./paths'
   file1=open(mapfile,'r')
   id=-1
   for line in file1:
    line=line.strip().split()
    if word==line[0].strip():
    	id=line[1].strip()
    	break
   file1.close()
   file2=open(paths,'r')
   ls=[]
   flag=0
   for line in file2:
   	line=line.strip().split()
   	if id==line[0].strip():
   		ls.append(line[1].strip())
   	elif id!=line[0].strip() and len(ls)>0:
   		break
   	else:
   		continue
   file2.close()
   return ls

if __name__ == '__main__':
  c=cluster('北京')
  for item in c:
     print item
