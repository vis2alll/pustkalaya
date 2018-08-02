page=1

KEY = 'D72551A2C3319E892DF355AAB1C55FCEEAE91A2236C39B931513155440537'
URL = 'https://library.daisyindia.org/NALP/rest/NALPAPIService/getNALPData/'


import os, sys, hashlib, base64, ftplib#, urllib.request, asyncio
import requests
from xml.dom import minidom

book_repo=[]
data = requests.get(URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=' + KEY, verify=False)
if(data.status_code == 200):       
    parsedData = minidom.parseString(data.text);
    books = parsedData.getElementsByTagName('result')
    if(len(books) == 0):
#                self.pcs._event.app.editor.message("No book found in sp.get_latest_books")
#                self.pcs._event.app.editor.focus(self.WINDOW)
        pass
        
    else:
        for book in books:
            row=[]
            
            
#                    book_id=book.getElementsByTagName('id')[0].firstChild.nodeValue
            
            for child in book.childNodes:
#              print child.localName
              if(len(child.childNodes)!=0) and child.tagName != "id":
                row.append(child.firstChild.nodeValue)
                
            row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
            book_repo.append(row)
#        print book_repo
        
        
else:
    
    msg="Error, server replied with"+ str(data.status_code)
    print str(msg)
