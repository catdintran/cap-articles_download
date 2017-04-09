#!/usr/bin/python

# Import modules for CGI handling 
import cgi
import myUtils
import requests
import re
from lxml import html
import json
import string
import pickle

############### Utils ###########

eco_url = 'http://www.economist.com/economics-a-to-z/'
# User-Agent to fake browser access
comon_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

def scrapEconomist(url):
    page = requests.get(url, headers=comon_header)
    return page.text
    
def scrapEconomistContent(url):
    page = requests.get(url, headers=comon_header)
    return html.fromstring(page.content)

def get_term_h2(tree):
    return tree.xpath('//div[@class="item-list"]//h2/text()')
    
def get_defintion_div(tree):
    definition =tree.xpath('//li//div[@class="content clearfix"]//text()')
    defList = []
    i = -1
    for d in definition:
        
        if d in ['\n    ']:
            i += 1
            defList.append('')
        if d not in ['\n  ']:
            defList[i] = defList[i] + d + ' '
    return defList    
    
def runRequestStep():
	return scrapEconomist(eco_url+"a")

def runMapStep():
	myDict={}
	alphabets = string.ascii_lowercase
	for a in alphabets:
	    web = eco_url + a   
	    tree = scrapEconomistContent(web)
	    terms = get_term_h2(tree)
	    definitions = get_defintion_div(tree)             
	    if len(terms) == len(definitions):
	        myDict.update({ a.upper()  : dict(zip(terms, definitions))})
	#        print(myDict)
	    else:
	        print(a)
	return myDict
	
############

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
step = form.getvalue('step')

ret_data=""
if step == "request":
	ret_data=runRequestStep()
	
if step == "map":
	dict_ret=runMapStep()
	# save dictionary to a pickle file
	pickle.dump(dict_ret,open( "alphabetDict.p", "wb" ))
	ret_data=str(dict_ret['A'])
	
if step == "clean":
	myDict = pickle.load( open( "alphabetDict.p", "rb" ) )
	for a in myDict:
		for k in myDict[a]:
			val = myDict[a][k]
			tmp_val = re.sub(r'\t|\r\n|\n|\'',"",val)
			myDict[a][k] = tmp_val
	pickle.dump(myDict,open( "alphabetDict.p", "wb" ))
	ret_data=str(myDict['A'])

if step=="alphabet":
	myChar = form.getvalue("character")
	myDict = pickle.load( open( "alphabetDict.p", "rb" ) )
	ret_data=str(myDict[myChar])

#print("Content-type:text/html\n")
print("Content-type:application/json")
print("")
response={"data": ret_data, "status": 1}
print(json.JSONEncoder().encode(response))


"""
print("<html>")
print("<head>")
print("<title>Hello - Second CGI Program</title>")
print("</head>")
print("<body>")
print("<h2>Hello</h2>")
print("<textarea>%s</textarea>" % (s_data))
print("</body>")
print("</html>")
"""