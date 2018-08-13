#page=100
#
#
##bookshare
#KEY='fh6re3gjwczpyx8f3xfzs8qr' # new 4 july
#URL = 'https://api.bookshare.org/book/'
##sugamya
#KEY = 'D72551A2C3319E892DF355AAB1C55FCEEAE91A2236C39B931513155440537'
#URL = 'https://library.daisyindia.org/NALP/rest/NALPAPIService/getNALPData/'
#
#
#
#import os, sys, hashlib, base64, ftplib#, urllib.request, asyncio
#import requests
#from xml.dom import minidom
#
#book_repo=[]
##bs
##data = requests.get(URL +"latest/limit/25/format/xml/page/" + str(page) + "?api_key=" + KEY, verify=False) # during production remove verify = false
##su
##data = requests.get(URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=' + KEY, verify=False)
##data = requests.get(URL + "popularbooks/noOfTimesDelivered/1/startDate/1010-01-01/endDate/3029-12-15/page/"+str(page)+"/limit/17/format/xml?API_key=" + KEY, verify=False) # during production remove verify = false
#data = requests.get(URL + "categorylist/page/"+str(page)+"/limit/52/format/xml?API_key=" + KEY, verify=False) # during production remove verify = false
#print data
#if(data.status_code == 200):       
#    parsedData = minidom.parseString(data.text.encode('utf-8'))
#    xml=parsedData.toxml('utf-8')
#    categories = parsedData.getElementsByTagName('title')
#    print xml
##    books = parsedData.getElementsByTagName('result')
##    print parsedData.getElementsByTagName('num-pages')[0].firstChild.nodeValue 
##    if(len(books) == 0):
##        s=parsedData.getElementsByTagName("string")        
##        for i in s:print i.firstChild.nodeValue                
###        print xml
###                self.pcs._event.app.editor.message("No book found in sp.get_latest_books")
###                self.pcs._event.app.editor.focus(self.WINDOW)
##        
##    else: 
##        total_books=parsedData.getElementsByTagName('total-results')[0].firstChild.nodeValue
##        print total_books
##        for i,book in enumerate(books):
###            if i==16:
##                row=[]
##                
##                
##                _id=book.getElementsByTagName('id')[0].firstChild.nodeValue
###                if str(_id)=="2133501":
##                
##                for child in book.childNodes:
##    #              print child.localName
##                  if(len(child.childNodes)!=0) and child.tagName != "id":
###                      pass
##                    row.append(child.firstChild.nodeValue)
##                author="author:::--"+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8'))    
##                row.append(author)                    
##                row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
##                book_repo.append(row)
###                print book.toxml('utf-8')
##                print book_repo[0]
###                    break
##        
##        
##else:
##    
##    msg="Error, server replied with"+ str(data.status_code)
##    print str(msg)
##
##
##
###<?xml version="1.0" encoding="utf-8"?><bookshare>
###  <status-code>11</status-code>
###  <version>5.5.9</version>
###  <messages>
###    <string>Results 0 - 0 of 109,951</string>
###    <string>Maximum page number possible is 440</string>
###  </messages>
###  <book>
###    <list>
###      <page>1416</page>
###      <limit>250</limit>
###      <num-pages>440</num-pages>
###    </list>
###  </book>
###</bookshare>
a=["1-f","1-q","123","ad"]
print a.remove("1-q")
print a

