# -*- coding: utf-8 -*- 
def createcluster():
   mapfile='/home/lizuyao2010/Downloads/brown-cluster-master/new_all_wiki-c1000-p1.out/map'
   paths='/home/lizuyao2010/Downloads/brown-cluster-master/new_all_wiki-c1000-p1.out/paths'
   file1=open(mapfile,'r')
   newfile1=open('map','w')
   newfile2=open('paths','w')
   for line in file1:
    line=line.strip().split()
    freq=int(line[6].strip())
    if freq>300:
      print >> newfile1, line[0].strip(),'\t',line[1].strip().rstrip('-L'),'\t',line[6].strip()
   file1.close()
   newfile1.close()

   file2=open(paths,'r')
   ls=[]
   flag=0
   for line in file2:
   	line=line.strip().split()
   	if int(line[2].strip())>300:
   		print >> newfile2, line[0].strip(),'\t',line[1].strip(),'\t',line[2].strip()
   file2.close()
   newfile2.close()

if __name__ == '__main__':
  createcluster()