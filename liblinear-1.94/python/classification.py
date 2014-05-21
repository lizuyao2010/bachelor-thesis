# -*- coding: utf-8 -*- 
#
# $Id: test.py 2055 2009-11-06 23:09:58Z shodan $
#
from math import *
from sphinxapi import *
import os,sys, time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 
import jieba.posseg as pseg
import operator
import jieba
from question_analysis import *
from probablity import *
from math import *
from cluster import *
from calculate import *

q = ''
mode = SPH_MATCH_ANY
host = 'localhost'
port = 9595
index = '*'
filtercol = 'group_id'
filtervals = []
sortby = ''
groupby = ''
groupsort = '@group desc'
limit = 40
path = '/usr/local/coreseek/var/zhwiki_Mar2012_xml/jian'
d = dict()

threshold = 200

#对数据建立索引
for fileName in os.listdir(path):
    filePath = path+'/'+fileName
    tree = ET.ElementTree(file=path+'/'+fileName)
    root = tree.getroot()
    for child in root:
        d[str(child.attrib['id'])]=filePath

#分词,词性标注，统计名词
def cuttest(test_sent,d2,d3,n):
    result = pseg.cut(test_sent)
    for w in result:
        if w.flag == 'ns' or w.flag == 'n' or w.flag == 'nr' or w.flag == 'nz' or w.flag == 'nt' or w.flag == 'ng' or w.flag == 'nrt':
            if w.word not in d2:
                d2[w.word]=1
            else:
                d2[w.word]+=1
            if w.word not in d3:
                d3[w.word]=dict()
            else:
                None
            if n not in d3[w.word]:
                d3[w.word][n]=1
            else:
                d3[w.word][n]+=1
def Query(q,maps,paths):
    contexts=question_analysis(q)
    sorted_d = []
    table=[]
    d2 = dict()
    d3 = dict()
    # 执行查询
    cl = SphinxClient()
    cl.SetServer ( host, port )
    cl.SetWeights ( [100, 1] )
    cl.SetMatchMode ( mode )
    if filtervals:
        cl.SetFilter ( filtercol, filtervals )
    if groupby:
	   cl.SetGroupBy ( groupby, SPH_GROUPBY_ATTR, groupsort )
    if sortby:
	   cl.SetSortMode ( SPH_SORT_EXTENDED, sortby )
    if limit:
	   cl.SetLimits ( 0, limit, max(limit,1000) )
    res = cl.Query ( q, index )
    log_f = open("retrieve.log","w")
    log_c = open("candidate.log","w") 
    if not res:
    	print 'query failed: %s' % cl.GetLastError()
    	sys.exit(1)

    if cl.GetLastWarning():
	   print 'WARNING: %s\n' % cl.GetLastWarning()

    print >> log_f, 'Query \'%s\' retrieved %d of %d matches in %s sec' % (q, res['total'], res['total_found'], res['time'])
    print >> log_f, 'Query stats:'

    if res.has_key('words'):
        for info in res['words']:
            print >> log_f, '\t\'%s\' found %d times in %d documents' % (info['word'], info['hits'], info['docs'])

    if res.has_key('matches'):
    	n = 1
    	print >> log_f, '\nMatches:'
    	for match in res['matches']:
    		filePath = d[str(match['id'])]
                tree = ET.ElementTree(file=filePath)
                match='article[@id="'+str(match['id'])+'"]'
                for elem in tree.iterfind(match):
                    print >> log_f, elem[0].text.encode('utf-8'), elem[1].text.encode('utf-8')
                    cuttest(elem[0].text.encode('utf-8').strip(),d2,d3,n)
                    lines = elem[1].text.encode('utf-8').strip().splitlines()
                
                for line in lines:
                    sents = line.strip().split('。')
                    for sen in sents:
                        cuttest(sen.strip(),d2,d3,n)    
                n += 1
        

        #候选词按词频从大到小排列
        sorted_d = sorted(d2.iteritems(),key=operator.itemgetter(1),reverse=True)
        f=open("debug.log",'w')
        i=1
        for w in sorted_d:
            if i>600:
                break
            name = w[0].encode('utf-8')
            c=[]
            if maps.has_key(name):
                identifier=maps[name]
            else:
                identifier=-1
            if paths.has_key(identifier):
                c=paths[identifier]
            else:
                c.append(name)
            tf = max(d3[w[0]].values())
            s = len(d3[w[0]])
            tfidf = tf*log(n-1/s)
            prob=1
            for y in contexts:
                if len(y)>5:
                    None#print >> f, q,name,y[0],y[1],y[2],y[3],y[4],y[5],probability_clusterInContext_givenCluster(c,y)
                else:
                    None#print >> f, q,name,y[0],y[1],y[2],probability_clusterInContext_givenCluster(c,y)
                prob*=probability_clusterInContext_givenCluster(c,y)#probability_wordInContext_givenWord(name,y)
            if prob==1:
                prob=0
            print >> f, name,'\t','1:'+str(w[1]),'\t','2:'+str(tf),'\t','3:'+str(prob)
            if prob>0:
                table.append([w[0],{1:w[1],2:tf},prob])
            i+=1
    else:
        print >> log_c, "no result"
    
    return table
        
#---------------------------------------------------
#
# $Id: test.py 2055 2009-11-06 23:09:58Z shodan $
#

if __name__=='__main__':
    maps,paths=loadCluster()
    table=Query('谁发明了元素周期表？',maps,paths)
