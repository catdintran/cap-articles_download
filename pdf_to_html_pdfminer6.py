# PDF to HTML (or TXT - commented out) formats with pdfminer.six

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
#import regex
import csv, re, os, sys
from timeit import default_timer as timer
import datetime as dt
#import multiprocessing

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    #retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    #device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    output = BytesIO()
    print("stage1")
    converter = HTMLConverter(rsrcmgr, output, codec=codec, laparams=LAParams())

    interpreter = PDFPageInterpreter(rsrcmgr, converter)
    print("stage2")
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    converter.close()
    print("stage3")
    #textstr = retstr.getvalue()
    convertedPDF = output.getvalue()
    print("stage4")
    #retstr.close()
    output.close()
    #device.close()
    return convertedPDF
    #return textstr


if __name__ == "__main__":
    # pdf files dir
    path1 = "U:\\***\\cap-articles_download\\"
    # final dir after converted
    path2 = "U:\\***\\cap-articles_download\\html\\"
 
    # placegholder for .pdf files
    doc_list = []
    
    # iterate through .pdf files from path1
    for pdfFile in os.listdir(path1):
        if pdfFile.endswith('.pdf'):
            doc_list.append(pdfFile)
    
    # iterate and process doc_list to html file
    for doc in doc_list:
        print("working with doc: {}".format(doc))
        fileHTML = doc.replace('pdf','html')
        pdfFile = path1 + doc
        
        scrape = open(pdfFile, 'rb')
        pdfFile = BytesIO(scrape.read())
        convertedPDF = readPDF(pdfFile)
        htmlFile = path2 + fileHTML
        fileConverted = open(htmlFile, "wb")
        fileConverted.write(convertedPDF)
        fileConverted.close()
        print("Done with file {}".format(fileHTML))
        
