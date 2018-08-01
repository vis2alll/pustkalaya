import os, sys, hashlib, base64, ftplib#, urllib.request
import requests
from xml.dom import minidom
#from prettytable import PrettyTable

from console.core.event_type import EventType

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass
    
from console.enums import DEFAULT_WINDOW
from _enums import BOOKLIST_WINDOW, LOGIN_WINDOW
from local_books import download_folder
### Class for BOOKSHARE  ###

class Bookshare():
#    KEY = 'xj4d2vektus5sdgqwtmq3tdc'
    KEY='fh6re3gjwczpyx8f3xfzs8qr'# new 4 july
    URL = 'https://api.bookshare.org/book/'

    def __init__(self,pcs):
        self.pcs = pcs
        self.WINDOW="BOOKLIST_WINDOW"
        self.userid = ''
        self.password = ''
        self.book_repo=[]
        self.book_details=[]
        self.detail_index=0
        self.latest_page=1
        self._on_search_ok=None
        self.search_input=""
        self.all_urls = {}
        self.category_name=""
        self.download_threads=[]
        self.login_status=False

    def check_credentials(self,userid,password):
        self.userid=userid
        self.password=password
        
        page=1
        try:
            data = requests.get(self.URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=' + self.KEY, verify=False)
            try:
                authString = self.userid + ":"+self.password
#                authString = "26353" + ':' +"9m85twwz"
                encoded = base64.b64encode(bytearray(authString.encode())).decode()
        #            print(id)
                headers = {'Authorization': 'Basic ' + encoded, "page" : "1", "limit" : "10", "format" : "xml", "API_key" : self.KEY}
                data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/fetchUserDownloadRequests", headers = headers, verify=False)
                if(data.status_code == 200):
                    parsedData = minidom.parseString(data.text)
#                    xml=parsedData.toxml('utf-8')
                    msg=parsedData.getElementsByTagName('message')
#                    self.pcs._event.app.editor.error("Error:"+str(msg))
                    if msg==[]:
                        return 1
                    else:
                        return "invalid credentials"
#                        self.pcs._event.app.editor.focus(BOOKLIST_WINDOW)
#                        self.pcs._event.current_window.buffer._files = [[str(xml)]]
#                        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                     
#                    self.pcs._event.app.editor.error("Error:"+str(data)+ str(data.status_code))
                else:
                    err="Error:"+str(data)+ str(data.status_code)
                    return err
#                    self.pcs._event.app.editor.error("Error:"+str(data)+ str(data.status_code))
            except:
                return str(e)[0:70]
          
        except IOError, e:
            return 'Network is unreachable'        

        except Exception as e:
#            self.pcs.menu_lvl="1"
#            self.pcs.get_user_input( self.pcs._event.app,self.pcs.reader_menu_lst)            
            
            return str(e)[0:70]

 

    def get_latest_books(self):
        # Get latest books from bookshare.org
        page=self.latest_page
        try:
            data = requests.get(self.URL + "latest/limit/25/format/xml/page/" + str(page) + "?api_key=" + self.KEY, verify=False) # during production remove verify = false

            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text.encode('utf-8'));
                books = parsedData.getElementsByTagName('result')
                if(len(books) == 0):
                    pass
                else:
                    for book in books:
                        row=[]
    #                    row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row.append( book.getElementsByTagName('author')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('title')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                        
#                        row=[]
#                        for child in book.childNodes:
#                            if(len(child.childNodes)!=0) and child.tagName != "id":
#                                c=child.firstChild.nodeValue
#                                if len(c)>=20:
#                                    for i in range(len(c)/20):
#                                        row.append(c[0+i*20:20+i*20])
#                                    row.append(c[(len(c)/20)*20:])
#                                else:
#                                    row.append(child.firstChild.nodeValue)
#                            
#                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
#                        self.book_repo.append(row)
                    
                self.menu_lvl="1-1"
                self.pcs._event.app.editor.focus(self.WINDOW)   
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
    #                if self.pcs._event.current_window.buffer.next_page==True :
    #                    self.pcs._event.app.editor.error("page"+str(self.latest_page))
                    
            else:
                self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))

        except IOError, e: 
            self.pcs.menu_lvl="1"
            self.pcs._event.app.editor.error('Network is unreachable')



    def get_popular_books(self):
        # Get popular books from bookshare.org
        page=self.latest_page
        try:
            data = requests.get(self.URL + "popular/limit/25/format/page/" + str(page) + "?api_key=" + self.KEY, verify=False) # during production remove verify = false
            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text.encode('utf-8'));
                books = parsedData.getElementsByTagName('result')
                if(len(books) == 0):
#                        print("No books found")
                    pass
                else:
                    for book in books:
                        row=[]
    #                    row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row.append( book.getElementsByTagName('author')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('title')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                    
                    self.pcs._event.app.editor.focus(self.WINDOW)        
                    self.pcs._event.current_window.buffer._files = self.book_repo
                    self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                            
                    self.latest_page+=1   
     
            else:
                self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))
                
        except IOError, e:
            self.pcs.menu_lvl="1"
            self.pcs._event.app.editor.error('Network is unreachable')
#            break
                    


    def _set_input_var(self,*args):
        
#        self.pcs._event.app.editor.error(str(type(args[0])))
        
        if str(args[-1])=="":
            self.get_search_input()
            
        self.search_input=str(args[-1])
        self.search_book()

        
    
    def get_search_input(self):
        self.pcs._event.current_window.buffer._files=[["No match found"]]
        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
        self.pcs._event.app.editor.input('search input:',
            "PROMPT_WINDOW",
            on_ok_handler = self._set_input_var)



    def search_book(self):
        # Search books by Title/Author from user given user input
        search=self.search_input
        page=self.latest_page
        try:
            data = requests.get(self.URL + "search/" + search + "/limit/25/format/page/" + str(page) + "?api_key=" + self.KEY, verify=False)# during production remove verify = false

            if(data.status_code == 200):       
                try:
                    parsedData = minidom.parseString(data.text.encode("utf-8"));
                except Exception as e:
#                    self.pcs._event.app.editor.error(str(e)[0:45])
                    return
                books = parsedData.getElementsByTagName('result')
                if(len(books) == 0):
#                        print("No books found")
                    pass
                else:
                    for book in books:
                        row=[]
    #                    row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row.append( book.getElementsByTagName('author')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('title')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                    
                    self.pcs.menu_lvl="1-3-b"                    
                    self.pcs._event.app.editor.focus(self.WINDOW)        
                    self.pcs._event.current_window.buffer._files = self.book_repo
                    self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                            
                    self.latest_page+=1   
     
            else:
                self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))
                
        except IOError, e:
            self.pcs.menu_lvl="1"
            self.pcs._event.app.editor.error('Network is unreachable')
#            break



   
    def get_book_categories(self):

#        self.book_repo=[]
        page=self.latest_page
        try:
            data = requests.get("https://api.bookshare.org/reference/category/list/limit/25/format/page/" + str(page) + "?api_key=" + self.KEY, verify=False) # during production remove verify = false
 
            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text.encode("utf-8"));
#                xml=parsedData.toxml('utf-8')
                
                categories = parsedData.getElementsByTagName('name')
#                print categories
                
                if(len(categories) == 0):
#                    print("No books found")
                    pass
                else:
                    count = 1+(self.latest_page-1)*10
#                    all_categories = {}
                    for category in categories:
                        self.book_repo.append([category.firstChild.nodeValue])
#                        all_categories[str(count)] = category.firstChild.nodeValue
                        count+=1
                    
                
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
#                self.pcs._event.current_window.buffer.reset()
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1                            
                    
 
            else:
                self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))
                
        except IOError, e:
            self.pcs.menu_lvl="1"
            self.pcs._event.app.editor.error('Network is unreachable')


    def category_book_search(self, category_name):
        page=self.latest_page
        try:
#            data = requests.get(self.URL + "category/" + category_name + "/format/page/?api_key=" + self.KEY, verify=False)           
            data = requests.get("https://api.bookshare.org/book/search/category/" + category_name + "/limit/52/format/page/" + str(page) + "?api_key=" + self.KEY, verify=False)           
            if(data.status_code == 200):
                parsedData = minidom.parseString(data.text.encode("utf-8"));
#                xml=parsedData.toxml('utf-8')
                books = parsedData.getElementsByTagName('result')

                if(len(books) == 0):
                    if page==1:
                        self.pcs._event.app.editor.error('No Books found')
                        self.book_repo=self.book_repo_temp
#                        self.pcs.menu_lvl="1-4"
                        return
                else:
                    for book in books:
                        row=[]
    #                    row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row.append( book.getElementsByTagName('author')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('title')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)

 
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
                if page==1:
                    self.pcs._event.current_window.buffer.reset()
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
                self.pcs.menu_lvl="1-4-b"
                                       
            else:
                self.pcs._event.app.editor.error("Error, server replied with"+ str(data.status_code))
                
        except IOError, e:
            self.pcs.menu_lvl="1"
            self.pcs._event.app.editor.error('Network is unreachable')        
        



    def get_by_book_id(self, id):
        # Search a particular book by ID
        try:
            data = requests.get(self.URL + "id/" + id + "/format/xml?api_key=" + self.KEY, verify=False)# during production remove verify = false
        except Exception as e:
            print(e)
        if(data.status_code == 200):       
            parsedData = minidom.parseString(data.text.encode('utf-8'));
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
                print("\n[d] To download book")
                print("[b] To go back")
                response = raw_input("Response: ")
            if(response != 'b'):
                self.book_download(id)
        else:
            print("Error, server replied with", data.status_code)


    def _on_password_ok(self,*args):
        self.password=str(args[-1])
        self.pcs._event.app.editor.error("Downloading...")
        self.start_download()
        
    def _on_userid_ok(self,*args):
        self.userid=str(args[-1])        
        
        self.pcs._event.app.editor.input('password:',
                    "PROMPT_WINDOW",
                    on_ok_handler = self._on_password_ok)        

    def get_login_credentials(self):
        self.pcs._event.app.editor.input('userid:',
                "PROMPT_WINDOW",
                on_ok_handler = self._on_userid_ok) 

  
                
    def book_download(self, id):
        
#        self.userid="vis2alll"
#        self.password="vis2alll"
        id=1932427 
        self.book_id=id
        if self.userid=="":
            self.get_login_credentials()
        else:
            self.pcs._event.app.editor.error("Downloading...")
            self.start_download()           
            
 

    def start_download(self):
        try:
            id=self.book_id
            
            
            m = hashlib.md5(str(self.password)).hexdigest()
            data = requests.get("https://api.bookshare.org/download/content/" + str(id) + "/version/1/for/"+
                str(self.userid)+"?api_key=" + self.KEY , headers={"X-password":m}, stream=True)# during production remove verify = false
 
            if data.status_code==200:
                if data.headers.get('content-type')=="application/zip":
                    current_dir= os.getcwd()
                    filename=data.headers.get("content-disposition").partition("=")[2]
                    final_dir= os.path.join(current_dir, str(download_folder)+str(filename)[:-4])
                    if not os.path.exists(final_dir):
                       os.makedirs(final_dir)                    
                    
                    import  zipfile, StringIO
                    z = zipfile.ZipFile(StringIO.StringIO(data.content))
                    z.extractall(final_dir)
        #                    z.extractall()
                    self.pcs._event.app.editor.error('Download completed '+str(filename)[0:50])
        
                elif data.headers.get('content-type').startswith("text/xml"):
                    self.userid=""
                    try:
                        parsedData = minidom.parseString(data.text.encode('utf-8'));
#                        sc=parsedData.getElementsByTagName('status-code')[0].firstChild.nodeValue
                        msg = parsedData.getElementsByTagName('string')
#                        xml=parsedData.toxml('utf-8')
                        str_lst=[]
                        for item in msg:
                            str_lst.append(str(item.firstChild.nodeValue))
                            
                        self.pcs.menu_lvl="1-m"
                        self.pcs.copy_buffer()
                        self.pcs._event.current_window.buffer._files = [str_lst]
            #            self.pcs._event.current_window.buffer.reset()
                        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                    except Exception as e:
                        self.userid=""
                        self.pcs._event.app.editor.error("Error: ",str(e)[0:50])
                else:
                    self.userid=""
                    self.pcs._event.app.editor.error(str(data.headers.get('content-type'))+"content-type not supported.")
           
                     
        except Exception as e:
            self.userid=""
            self.pcs._event.app.editor.error("Netowrk unreachable")


    def logout(self):
        self.login_status=False
        self.userid=""
        self.password=""