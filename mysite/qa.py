# -*- coding: utf-8 -*- 	
try:
    import xml.etree.cElementTree as ET
except ImportError:  
    import xml.etree.ElementTree as ET
 
path = '/usr/local/coreseek/var/zhwiki_Mar2012_xml'
d = dict()
tree = ET.parse(path+'/all_questions.xml')
def set_qa():
	for qa in tree.iterfind('QA'):
	    question = ""
	    answers = []
	    for q in qa.iterfind('QUESTION/Q[@LANG="ZH"]'):
	    	question = q.text.encode('utf-8')
	    for q in qa.iterfind('ANSWER/A[@LANG="ZH"]'):
	    	answers.append(q.text.encode('utf-8'))
	    d[question]=answers
	return d


