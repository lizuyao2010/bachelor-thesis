# -*- coding: utf-8 -*-
# deal with word's children
def dealwithchildren(word,sent):
    ID=word[0]
    PLemma=word[1]
    PPOS=word[2]
    PHead=word[3]
    PDeprel=word[4]
    if (PPOS=='NR'or PPOS=='NN'):
        triplelist=[]
        for wordj in sent:
            PLemmaj=wordj[1]
            PPOSj=wordj[2]
            PHeadj=wordj[3]
            PDeprelj=wordj[4]
            if PHeadj==ID and (PPOSj=='NN'or PPOSj=='NR'):
                triple=(PLemmaj,'X',PDeprelj)
                triplelist.append(triple)
        return triplelist
        

def dealwithparent(word,sent):
    ID=word[0]
    PLemma=word[1]
    PPOS=word[2]
    PHead=word[3]
    PDeprel=word[4]
    triplelist=[]

    if (PPOS=='NR'or PPOS=='NN') and (int(PHead)>0):
        Parent = sent[int(PHead)-1]
        triple=('X',Parent[1],PDeprel)
        
        triplelist.append(triple)
        # deal with his siblings
        for wordj in sent:
            if wordj[3] == Parent[0] and wordj[0] != ID and (wordj[2]=='NN'or wordj[2]=='NR'):
                triple2=('X',Parent[1],PDeprel,wordj[1],Parent[1],wordj[4])
                triplelist.append(triple2)
        
        return triple,triplelist
    else:
        return (),[]

def dealwithgrandchildren(word,sent):
    ID=word[0]
    PLemma=word[1]
    PPOS=word[2]
    PHead=word[3]
    PDeprel=word[4]
    triplelist=[]
    if (PPOS=='NR'or PPOS=='NN'):
        for wordi in sent:
            if wordi[3]==ID:
                for wordj in sent:
                    if wordj[3]==wordi[0] and (wordj[2]=='NR' or wordj[2]=='NN'):
                        triple = (wordj[1],wordi[1],wordj[4],wordi[1],'X',wordi[4])
                        triplelist.append(triple)
    return triplelist

if __name__ == '__main__':
    f = open("/home/lizuyao2010/wiki/question_context.table",'r')
    fw = open("sixple1.txt",'w')
    fw2 = open("sixple2.txt","w")
    d=dict()
    d2=dict()
    sent=[]
    for line in f:
        line=line.strip()
        if line=='':
            for word in sent:
                N2Xs=dealwithchildren(d,d2,word,sent)
                X2P=dealwtihparent(d,d2,word,sent)
                prevN2X=()
                if N2Xs:
                    for N2X in N2Xs:
                        if N2X and prevN2X:
                            N2XN2X = (N2X[0],N2X[1],N2X[2],prevN2X[0],prevN2X[1],prevN2X[2])
                            addkeyvalue(word[1],d,d2,N2XN2X)
                        if N2X and X2P:
                            N2X2P = (N2X[0],N2X[1],N2X[2],X2P[0],X2P[1],X2P[2])
                            addkeyvalue(word[1],d,d2,N2X2P)
                        prevN2X = N2X
                dealwithgrandchildren(d,d2,word,sent)

            sent=[]#if line=='' over
        elif line.isdigit():
            None# articles.append(article)
        else:
            table=line.split('\t')
            ID = table[0]
            PLemma = table[3]
            PPOS = table[5]
            PHead = table[9]
            PDeprel = table[11]
            sent.append((ID,PLemma,PPOS,PHead,PDeprel))    

    for row in d.items():
        print >> fw,row[0]+'\t',
        for col in row[1].items():
            if int(col[1])>0:
                if len(col[0])>5:
                    print >> fw,col[0][0],col[0][1],col[0][2],col[0][3],col[0][4],col[0][5],':',col[1],'\t',
                else:
                    print >> fw,col[0][0],col[0][1],col[0][2],':',col[1],'\t',
        print >> fw

    for row in d2.items():
        if int(row[1])>0:
            if len(row[0])>5:
                print >> fw2,row[0][0],row[0][1],row[0][2],row[0][3],row[0][4],row[0][5],'\t',row[1]
            else:
                print >> fw2,row[0][0],row[0][1],row[0][2],'\t',row[1]