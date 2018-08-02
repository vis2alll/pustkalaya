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
import threading
### Class for BOOKSHARE  ###

class Bookshare():
#    KEY = 'xj4d2vektus5sdgqwtmq3tdc'
    KEY='fh6re3gjwczpyx8f3xfzs8qr'# new 4 july
    URL = 'https://api.bookshare.org/book/'

    def __init__(self,pcs):
        self.pcs = pcs
        self.WINDOW="BOOKLIST_WINDOW"
        self.userid =None
        self.password =None
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
        
        
        self.count=1#


    def get_latest_books(self):
        # Get latest books from bookshare.org
        page=self.latest_page
#        self.pcs.copy_buffer()
        try:
            data = requests.get(self.URL + "latest/limit/25/format/xml/page/" + str(page) + "?api_key=" + self.KEY, verify=False) # during production remove verify = false

            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text.encode('utf-8'));
                
#                xml=parsedData.toxml('utf-8')                    
#                self.pcs._event.current_window.buffer._files = [[xml]]
#                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
#                return

                books = parsedData.getElementsByTagName('result')
                if(len(books) == 0):
                    pass
                else:
                    for book in books:
                        row=[]
                        row.append('author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')))
                        synopsis = str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8'))                        
                        if(len(synopsis) != 0):
                            row.append("synopsis:"+synopsis)
#                        row.append('brief-synopsis:'+str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('id:'+str(book.getElementsByTagName('id')[0].firstChild.nodeValue.encode('utf-8')))
                        self.book_repo.append(row)
                    
                self.menu_lvl="1-1"
                self.pcs._event.app.editor.focus(self.WINDOW)   
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
    #                if self.pcs._event.current_window.buffer.next_page==True :
    #                    self.pcs._event.app.editor.error("page"+str(self.latest_page))
                    
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg) 
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')          
         

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
                        row.append('author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')))
                        synopsis = str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8'))                        
                        if(len(synopsis) != 0):
                            row.append("synopsis:"+synopsis)
#                        row.append('brief-synopsis:'+str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('id:'+str(book.getElementsByTagName('id')[0].firstChild.nodeValue.encode('utf-8')))
                        self.book_repo.append(row)
                    
                    self.pcs._event.app.editor.focus(self.WINDOW)        
                    self.pcs._event.current_window.buffer._files = self.book_repo
                    self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                            
                    self.latest_page+=1   
                    
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')          
         

    def _set_input_var(self,*args):
#        self.pcs._event.app.editor.error(str(type(args[0])))
        self.search_input=str(args[-1])
        self.pcs.menu_lvl = "1-3"
        self.search_book()

        
    
    def get_search_input(self):
        self.pcs.menu_lvl = "1-3-e"
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
                        row.append('author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')))
                        synopsis = str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8'))                        
                        if(len(synopsis) != 0):
                            row.append("synopsis:"+synopsis)
#                        row.append('brief-synopsis:'+str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('id:'+str(book.getElementsByTagName('id')[0].firstChild.nodeValue.encode('utf-8')))
                        self.book_repo.append(row)

                    
                    self.pcs.menu_lvl="1-3-b"                    
                    self.pcs._event.app.editor.focus(self.WINDOW)        
                    self.pcs._event.current_window.buffer._files = self.book_repo
                    self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                            
                    self.latest_page+=1   
     
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                   
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')            

   
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
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')        
         

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
                        row.append('author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')))
                        synopsis = str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8'))                        
                        if(len(synopsis) != 0):
                            row.append("synopsis:"+synopsis)
#                        row.append('brief-synopsis:'+str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8')))
                        row.append('id:'+str(book.getElementsByTagName('id')[0].firstChild.nodeValue.encode('utf-8')))
                        self.book_repo.append(row)



 
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
                if page==1:
                    self.pcs._event.current_window.buffer.reset()
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
                self.pcs.menu_lvl="1-4-b"
                
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')          


    def get_book_id(self, id):
        # Search a particular book by ID
        try:
            data = requests.get(self.URL + "id/" + str(id) + "/format/xml?api_key=" + self.KEY, verify=False)# during production remove verify = false
 
            if(data.status_code == 200): 
                row=[]
                parsedData = minidom.parseString(data.text.encode('utf-8'));

#                        row=[]
#                        row.append('author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8')))
#                        row.append('title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')))
##                        row.append('brief-synopsis:'+str(book.getElementsByTagName('brief-synopsis')[0].firstChild.nodeValue.encode('utf-8')))
#                        row.append('id:'+str(book.getElementsByTagName('id')[0].firstChild.nodeValue.encode('utf-8')))
#                        self.book_repo.append(row)

                title = 'title:'+str(book.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8'))
                author = 'author:'+str(book.getElementsByTagName('author')[0].firstChild.nodeValue.encode('utf-8'))
                synopsis = "synopsis:"+parsedData.getElementsByTagName('brief-synopsis')[0].encode('utf-8')
                row.append(title)
                row.append(author)
                
                if(len(synopsis.childNodes) != 0):
                    row.append(synopsis.firstChild.nodeValue) 
                row.append(id)
                self.book_repo=[row]
                self.pcs._event.app.editor.focus(self.WINDOW) 
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.reset()
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
    
                    
                    
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable') 


    def _on_password_ok(self,*args):
        self.password=str(args[-1])
        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
#        self.pcs.copy_buffer()
#        go_to_prev_state        
        
        self.pcs._event.app.editor.error("Downloading.")
               
        
        self.star_download_thread()
        
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
        if self.count==1:
            id=1930029
            self.count+=1
        elif self.count==2:
            id=1932427
            self.count+=1
        else:
            id=1930040
            self.count=1
        self.book_id=id
        if self.userid==None:
            self.get_login_credentials()
        else:
            self.pcs._event.app.editor.error("Downloading...")
            self.star_download_thread()   
            
    def star_download_thread(self):            
        
        t=threading.Thread(target=self.start_download)
        t.start()
        self.download_threads.append(t) 

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
                    self.userid=None
                    try:
                        parsedData = minidom.parseString(data.text.encode('utf-8'));
#                        sc=parsedData.getElementsByTagName('status-code')[0].firstChild.nodeValue
                        msg = parsedData.getElementsByTagName('string')
#                        xml=parsedData.toxml('utf-8')
                        str_lst=[]
                        for item in msg:
                            str_lst.append(str(item.firstChild.nodeValue))
                            
                        self.pcs.menu_lvl="1-m"
                        self.pcs._event.app.editor.focus(self.WINDOW) 
                        self.pcs._event.current_window.buffer._files = [str_lst]
                        self.pcs._event.current_window.buffer.reset()
                        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
#                        self.pcs.copy_buffer()
                        
                        
                    except Exception as e:
                        self.userid=None
                        self.pcs.menu_lvl="1-e"
                        msg=str(e)#"Network unreachable"
                        self.pcs.show_msg(msg)
#                        exc_type, exc_obj, exc_tb = sys.exc_info()
#                        self.pcs._event.app.editor.error("345: "+str(exc_type))        



         
                else:
                    self.userid=None
                    self.pcs.menu_lvl="1-e"
                    msg=str(data.headers.get('content-type'))+"content-type not supported."
                    self.pcs.show_msg(msg)

        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
 
            exc_type, exc_obj, tb = sys.exc_info()
            lineno = tb.tb_lineno
            msg=str(e)+str(lineno)#"Network unreachable"
            self.pcs._event.app.editor.error(msg) 
#            self.pcs.show_msg(msg)
            
           
         

    def logout(self):
        choice="2"
        self.pcs.choice_selection(self.pcs._event, choice)        
        self.login_status=False
        self.userid=None
        self.password=None
        self.pcs._event.app.editor.error('logged out of bookshare')