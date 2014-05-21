# -*- coding: utf-8 -*-
def returndict1(fileName):
    f=open(fileName,'r')
    d=dict()
    n=0
    num=0
    for line in f:
        row = line.strip().split('\t')
        if len(row)==1:
            continue
        if d.has_key(row[0]):
            None
        else:
            d[row[0]]=dict()
        for col in row[1:]:
            keyvalue=col.strip().split(':')
            key=keyvalue[0].strip().split()
            if len(key)>5:
            	triple=(key[0],key[1],key[2],key[3],key[4],key[5])
                value=int(keyvalue[1].strip())
                d[row[0]][triple]=value
            elif len(key)>2:
                triple=(key[0],key[1],key[2])
                if keyvalue[1].strip().isdigit():
                    value=int(keyvalue[1].strip())
                    d[row[0]][triple]=value
            else:
                n+=1
                #print "Error:key is shorter than 3"
            num+=1
    #print n,num,float(n)/num
    return d

def returndict2(fileName):
    d=dict()
    n=0
    num=0
    f = open(fileName,'r')
    for line in f:
        row=line.strip().split('\t')
        if len(row)==1:
            continue
        key=row[0].strip().split()
        if len(key)>5:
            triple=(key[0],key[1],key[2],key[3],key[4],key[5])
            value=int(row[1].strip())
            d[triple]=value
        elif len(key)>2:
            triple=(key[0],key[1],key[2])
            value=int(row[1].strip())
            d[triple]=value
        else:
           n+=1
           #print "Error:key is shorter than 3"
        num+=1
    #print n,num,float(n)/num
    return d
if __name__ == '__main__':
    d1 = returndict1("sixple1.txt")
    print d1['中国'][('X','是','PRD','国家', '是', 'SBJ')]
    #中国的首都是哪里？
    #d2 = returndict2('sixple2.txt')
    #print d['X','车','AMOD']
