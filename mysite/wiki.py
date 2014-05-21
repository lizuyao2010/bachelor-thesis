# -*- coding: utf-8 -*- 
#
# $Id: test.py 2055 2009-11-06 23:09:58Z shodan $
#

from sphinxapi import *
import os,sys, time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 
import jieba.posseg as pseg
import operator
import jieba

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
def cuttest(test_sent,d2):
    result = pseg.cut(test_sent)
    for w in result:
        if w.flag == 'ns' or w.flag == 'n' or w.flag == 'nr' or w.flag == 'nz' or w.flag == 'nt' or w.flag == 'ng' or w.flag == 'nrt':
            if w.word not in d2:
                d2[w.word]=1
            else:
                d2[w.word]+=1
def Query(q):
    sorted_d = []
    d2 = dict()
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
		attrsdump = ''
		for attr in res['attrs']:
			attrname = attr[0]
			attrtype = attr[1]
			value = match['attrs'][attrname]
			if attrtype==SPH_ATTR_TIMESTAMP:
				value = time.strftime ( '%Y-%m-%d %H:%M:%S', time.localtime(value) )
			attrsdump = '%s, %s=%s' % ( attrsdump, attrname, value )

		print >> log_f, '%d. doc_id=%s, weight=%d%s' % (n, match['id'], match['weight'], attrsdump)
		filePath = d[str(match['id'])]
                tree = ET.ElementTree(file=filePath)
                match='article[@id="'+str(match['id'])+'"]'
                for elem in tree.iterfind(match):
                    print >> log_f, elem[0].text.encode('utf-8'), elem[1].text.encode('utf-8')
                    cuttest(elem[0].text.encode('utf-8').strip(),d2)
                    lines = elem[1].text.encode('utf-8').strip().splitlines()
		    
                    for line in lines:
                        sents = line.split('。')
                        for sen in sents:
                            cuttest(sen,d2)
                n += 1
        #候选词按词频从大到小排列
        sorted_d = sorted(d2.iteritems(),key=operator.itemgetter(1),reverse=True)
        n = 1
        for w in sorted_d:
            print >> log_c, w[0].encode('utf-8'), w[1]
            if n >= threshold:
                break
            n += 1
    else:
        print >> log_c, "no result"
    
    return sorted_d
        
#---------------------------------------------------
#
# $Id: test.py 2055 2009-11-06 23:09:58Z shodan $
#

