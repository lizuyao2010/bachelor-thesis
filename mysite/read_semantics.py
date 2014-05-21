# -*- coding: utf-8 -*-
def addkeyvalue(key1,d,d2,key2):
    if d.has_key(key1):
        None
    else:
        d[key1]=dict()
    if d[key1].has_key(key2):
        d[key1][key2]+=1
    else:
        d[key1][key2]=1
    if d2.has_key(key2):
        d2[key2]+=1
    else:
        d2[key2]=1

if __name__ == '__main__':
    f = open("/home/lizuyao2010/wiki/question_context.table",'r')
    fw = open("sem_triple1.txt",'w')
    fw2 = open("sem_triple2.txt","w")
    d=dict()
    d2=dict()
    sent=[]
    for line in f:
        line=line.strip()
        if line=='' and sent:
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
                        pair=('X',verb)
                        addkeyvalue(A0,d,d2,pair)
                        if A1:
                            triple=('X',verb,A1)
                            addkeyvalue(A0,d,d2,triple)
                            triple=(A0,verb,'X')
                            addkeyvalue(A1,d,d2,triple)
                    else:
                        if A1:
                            pair=(verb,'X')
                            addkeyvalue(A1,d,d2,pair)


            sent=[]#if line=='' over
        elif line.isdigit():
            None
        else:
            table=line.split('\t')
            if len(table)>14:    
                sent.append(table)    

    for row in d.items():
        print >> fw,row[0]+'\t',
        for col in row[1].items():
            if int(col[1])>0:
                if len(col[0])>2:
                    print >> fw,col[0][0],col[0][1],col[0][2],':',col[1],'\t',
                else:
                    print >> fw,col[0][0],col[0][1],':',col[1],'\t',
        print >> fw

    for row in d2.items():
        if int(row[1])>0:
            if len(row[0])>2:
                print >> fw2,row[0][0],row[0][1],row[0][2],'\t',row[1]
            else:
                print >> fw2,row[0][0],row[0][1],'\t',row[1]