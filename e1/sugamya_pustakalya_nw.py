import os, sys, hashlib, base64, ftplib#, urllib.request, asyncio
import requests
from xml.dom import minidom
from prettytable import PrettyTable

#-----------------------------
from console.core.event_type import EventType
from console.ui.menu_window import Menu, MenuItem
from console.enums import DEFAULT_WINDOW


class SugamyaPustakalya():


    KEY = 'D72551A2C3319E892DF355AAB1C55FCEEAE91A2236C39B931513155440537'
    URL = 'https://library.daisyindia.org/NALP/rest/NALPAPIService/getNALPData/'
 
    
    
    def __init__(self,pcs):
        self.pcs = pcs
        self.WINDOW="BOOKLIST_WINDOW"
        self.userid = ''
        self.password = ''
        self.book_repo=[]
        self.book_details=[]
        self.detail_index=0
        self.latest_page=1



    def get_latest_books(self):
        
 
#        c_win=self.pcs._event.app.editor.current_window #"str(self.pcs._event.app.editor.current_window)"
        
        page=self.latest_page
        try:
            data = requests.get(self.URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=\
                                ' + self.KEY, verify=False)
            
            
        except Exception as e:
            self.pcs._event.app.editor.message('%s %s' % ("Error,",str(e)))
            
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text);
            books = parsedData.getElementsByTagName("result")
            
            if(len(books) == 0):
                self.pcs._event.app.editor.message("No book found :"+str(parsedData.getElementsByTagName('result')))
#                self.pcs._event.app.editor.focus("BOOKLIST_WINDOW")
            else:
                
                for book in books:
                    row=[]
#                    book_id=book.getElementsByTagName('id')[0].firstChild.nodeValue
                    for child in book.childNodes:
                      if(len(child.childNodes)!=0) and child.tagName != "id":
                        row.append(child.firstChild.nodeValue[:20])
                        
                    row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                    self.book_repo.append(row)
                    
                self.pcs._event.app.editor.focus(self.WINDOW)   
                self.pcs._event.current_window.buffer._files = self.book_repo
                                
                self.latest_page+=1
        else:
            self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))


    def get_popular_books(self, page):
        # Get popular books from Sugamya Pustakalya
        try:
            data = requests.get(self.URL + "popularbooks/noOfTimesDelivered/1/startDate/2017-01-01/endDate/2017-12-15/page/1/limit/17/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false
        except Exception as e:
            print(e)
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text);
            books = parsedData.getElementsByTagName('result')
            if(len(books) == 0):
                print("No books found")
            else:
                all_ids = []
                t = PrettyTable(['AUTHOR', 'BRIEF-SYNOPSIS', 'DOWNLOAD-FORMAT','DTBOOK-SIZE', 'FREELY-AVAILABLE', 'ID', 'ISBN13', 'TITLE'])
                
                for book in books:
                    row=[]
                    for child in book.childNodes:
                      if(len(child.childNodes)!=0):
                        row.append(child.firstChild.nodeValue[:20])
                      else:
                        row.append('NA')
                    if(len(row) == 8):
                        t.add_row(row)
                    all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                t.align = "l"
                print(t)
                response = ''
                while(response not in all_ids and response != 'b' and response != 'n'):
                    if(response != ''):
                        print("\nInvalid choice, try again")
                    print("\nEnter a book ID to search and download")
                    print("\nEnter n to display next page")
                    print("Enter b to go back")
                    response = raw_input("\nResponse: ")
                if(response  == 'n'):
                    self.get_popular_books(page + 1)
                elif(response != 'b'):
                    self.get_book_id(response)
        else:
            print("Error, server replied with", data.status_code)


    def get_book_categories(self, page):
        # Get popular books from Sugamya Pustakalya
        try:
            data = requests.get(self.URL + "categorylist/page/1/limit/52/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false
        except Exception as e:
            print(e)
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text);
            categories = parsedData.getElementsByTagName('title')
            if(len(categories) == 0):
                print("No books found")
            else:
                print("BOOK CATEGORIES")
                all_categories = []
                for category in categories:
                    print(category.firstChild.nodeValue)
                    all_categories.append(category.firstChild.nodeValue)
                response = ''
                while(response not in all_categories and response != 'b'):
                    if(response != ''):
                        print("\nInvalid choice, try again")
                    print("\nEnter a book category to search")
                    print("Enter b to go back")
                    response = raw_input("\nResponse: ")
                if(response != 'b'):
                    self.category_search(response,1)
        else:
            print("Error, server replied with", data.status_code)

    def category_search(self, category_name, page):
        # Get books of a particular category

        try:
            data = requests.get(self.URL + "category/" + category_name + "/page/1/limit/52/format/xml?API_key=" + self.KEY, verify=False)
        except Exception as e:
            print(e)
        if(data.status_code == 200):
            parsedData = minidom.parseString(data.text);
            books = parsedData.getElementsByTagName('result')
            if(len(books) == 0):
                print("No books found")
            else:
                all_ids = []
                t = PrettyTable(['AUTHOR', 'BRIEF-SYNOPSIS', 'DOWNLOAD-FORMAT','DTBOOK-SIZE', 'FREELY-AVAILABLE', 'ID', 'ISBN13', 'TITLE'])
                
                for book in books:
                    row=[]
                    for child in book.childNodes:
                      if(len(child.childNodes)!=0):
                        row.append(child.firstChild.nodeValue[:20])
                      else:
                        row.append('NA')
                    if(len(row) == 8):
                        t.add_row(row)
                    all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                t.align = "l"
                print(t)
                response = ''
                while(response not in all_ids and response != 'b' and response != 'n'):
                    if(response != ''):
                        print("\nInvalid choice, try again")
                    print("\nEnter a book ID to search and download")
                    print("\nEnter n to display next page")
                    print("Enter b to go back")
                    response = raw_input("\nResponse: ")
                if(response  == 'n'):
                    self.get_latest_books(page + 1)
                elif(response != 'b'):
                    self.get_book_id(response)
        else:
            print("Error, server replied with", data.status_code)

    def search_book(self, page):
        # Search books by Title/Author from user given user input
        search = raw_input("Enter book Title/Author: ")
        try:
            data = requests.get(self.URL + "authortitle/" + search + "/page/1/limit/25/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false
        except Exception as e:
            print(e)
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text);
            books = parsedData.getElementsByTagName('result')
            if(len(books) == 0):
                print("No books found")
            else:
                all_ids = []
                t = PrettyTable(['AUTHOR', 'BRIEF-SYNOPSIS', 'DTBOOK-SIZE','FREELY-AVAILABLE', 'ID', 'ISBN13', 'PUBLISHER', 'TITLE'])
                
                for book in books:
                    row=[]
                    for child in book.childNodes:
                      if(len(child.childNodes)!=0):
                        row.append(child.firstChild.nodeValue[:20])
                      else:
                        row.append('NA')
                    if(len(row) == 8):
                        t.add_row(row)
                    all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                t.align = "l"
                print(t)
                response = ''
                while(response not in all_ids and response != 'b' and response != 'n'):
                    if(response != ''):
                        print("\nInvalid choice, try again")
                    print("\nEnter a book ID to search and download")
                    print("\nEnter n to display next page")
                    print("Enter b to go back")
                    response = raw_input("\nResponse: ")
                if(response  == 'n'):
                    self.get_latest_books(page + 1)
                elif(response != 'b'):
                    self.get_book_id(response)
        else:
            print("Error, server replied with", data.status_code)

    def get_book_id(self, id):
        # Search a particular book by ID
        try:
            data = requests.get(self.URL + "id/" + id + "/page/1/limit/25/format/xml?API_key=" + self.KEY, verify=False)# during production remove verify = false
        except Exception as e:
            print(e)
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text);
            title = parsedData.getElementsByTagName('title')[0].firstChild.nodeValue
            author = parsedData.getElementsByTagName('author')[0].firstChild.nodeValue
            synopsis = parsedData.getElementsByTagName('brief-synopsis')[0]
            print("\nTitle: " + title)
            print("Author: " + author)
            if(len(synopsis.childNodes) != 0):
                print("Synopsis: " + synopsis.firstChild.nodeValue) 

            response = ''
            while(response != 'd' and response != 'b'):
                if(response != ''):
                    print("\nInvalid choice")
                print("\n[d] To make download book request")
                print("[b] To go back")
                response = raw_input("Response: ")
            if(response != 'b'):
                self.book_download_request(id)
        else:
            print("Error, server replied with", data.status_code)

    def book_download_request(self, id):
        # Download a book
        # if(self.userid == '' or self.password == ''):
        #     self.login()
        try:
            authString = "26353" + ':' "9m85twwz"
            encoded = base64.b64encode(bytearray(authString.encode())).decode()
            print(id)
            headers = {'Authorization': 'Basic ' + encoded, "page" : "1", "limit" : "1", "format" : "xml", "API_key" : self.KEY, "bookId" : id, "formatId" : '6'}
            data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/raiseBookDownloadRequest", headers = headers, verify=False)
        except Exception as e:
            print "err: in book_download_request",(e)

        if(data.status_code == 200):
            parsedData = minidom.parseString(data.text)
            if parsedData.getElementsByTagName('message')!=[]:
                message = parsedData.getElementsByTagName('message')[0]
                print(message.firstChild.nodeValue)
            else:
                print "Not available to download"
        else:
            print("Error, server replied with", data.status_code) 

    def download_books(self):
        # download books that are ready for downloading
        try:
            authString = "26353" + ':' "9m85twwz"
            encoded = base64.b64encode(bytearray(authString.encode())).decode()
            print(id)
            headers = {'Authorization': 'Basic ' + encoded, "page" : "1", "limit" : "10", "format" : "xml", "API_key" : self.KEY}
            data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/fetchUserDownloadRequests", headers = headers, verify=False)
        except Exception as e:
            print(e)

        if(data.status_code == 200):
            parsedData = minidom.parseString(data.text)
            print(parsedData.toxml())
            count = 1
            all_urls = {}
            books = parsedData.getElementsByTagName('result')
            t = PrettyTable(['ID', 'TITLE', 'STATUS'])
            for book in books:
                status = book.getElementsByTagName('available-to-download')[0].firstChild.nodeValue
                t.add_row([count, book.getElementsByTagName('title')[0].firstChild.nodeValue, status])
                if(status == 'Available for Download'):
                    all_urls[str(count)] = book.getElementsByTagName('downloadUrl')[0].firstChild.nodeValue
                count += 1
            t.align = "l"
            print(t)
            response = ''
            while(response not in all_urls and response != 'b'):
                if(response != ''):
                    print("\nInvalid choice")
                print("\nEnter Book ID to download an available book")
                print("[b] To go back")
                response = raw_input("Response: ")

            if(response != 'b'):
                path = ''
                url = all_urls[response].split('/')
                host = url[2].split(':')[0]
                port = url[2].split(':')[1]
                filename = url[4]
                ftp = ftplib.FTP(host) 
                ftp.login("26353", "9m85twwz") 
                ftp.cwd(path)
                ftp.retrbinary("RETR " + url[3] + "/" + url[4], open(filename, 'wb').write)
                ftp.quit()
                # proxy = urllib.request.ProxyHandler({'http': 'proxy22.iitd.ac.in:3128'})
                # opener = urllib.request.build_opener(proxy)
                # urllib.request.install_opener(opener)
                # with closing(urllib.request.urlopen(all_urls[response])) as r:
                #     with open('file', 'wb') as f:
                #         shutil.copyfileobj(r, f)
        else:
            print("Error, server replied with", data.status_code)

    def login(self):
        USERID = raw_input("User ID/ Email: ")
        PASSWORD = raw_input("Password: ")


