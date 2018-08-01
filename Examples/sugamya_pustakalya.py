import os, sys, hashlib, base64, ftplib#, urllib.request, asyncio
import requests
from xml.dom import minidom
#from prettytable import PrettyTable

#-----------------------------------------------

from console.core.event_type import EventType

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass
    
from console.enums import DEFAULT_WINDOW
from _enums import BOOKLIST_WINDOW, LOGIN_WINDOW
from local_books import download_folder

class SugamyaPustakalya():

    KEY = 'D72551A2C3319E892DF355AAB1C55FCEEAE91A2236C39B931513155440537'
    URL = 'https://library.daisyindia.org/NALP/rest/NALPAPIService/getNALPData/'


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
                headers = {'Authorization': 'Basic ' + encoded, "page" : "1", "limit" : "10", "format" : "xml", "API_key" : self.KEY}
                data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/fetchUserDownloadRequests", headers = headers, verify=False)
 
                if(data.status_code == 200):
                    parsedData = minidom.parseString(data.text)
                    msg=parsedData.getElementsByTagName('message')

                    if msg==[]:
                        return 1
                    else:
                        return "invalid credentials..."
                else:
                    err="Error:"+str(data)+ str(data.status_code)
                    return err
                    
            except Exception as e:
                return str(e.message)

        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')           
                     



    def get_latest_books(self):
        page=self.latest_page
        self.pcs.menu_lvl="1-1"
        
#        self.book_repo=[]
#        pages=[i for i in range(1,5)]
#        
#        for page in pages: 

#            data = requests.get(self.URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=' + self.KEY, verify=False)
        try:
            data = requests.get(self.URL + 'latest/page/' + str(page) + '/limit/20/format/JSON?API_key=' + self.KEY, verify=False)
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
                          if(len(child.childNodes)!=0) and child.tagName != "id":
                            row.append(child.firstChild.nodeValue)
                            
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                    
    #                if self.latest_page==1:
#                self.menu_lvl="1-1"
                self.pcs._event.app.editor.focus(self.WINDOW)   
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
                self.pcs.copy_buffer()
    #                if self.pcs._event.current_window.buffer.next_page==True :
    #                    self.pcs._event.app.editor.error("page"+str(self.latest_page))
                    
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)


        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')          
         

    def get_popular_books(self):
        # Get popular books from Sugamya Pustakalya
#        self.book_repo=[]
        page=self.latest_page
#        pages=[i for i in range(1,2)]
#        
#        for page in pages:
        try:
            data = requests.get(self.URL + "popularbooks/noOfTimesDelivered/1/startDate/2017-01-01/endDate/2017-12-15/page/"+str(page)+"/limit/17/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false
            
            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text);
                books = parsedData.getElementsByTagName('result')
                if(len(books) == 0):
#                        print("No books found")
                    pass
                else:
#                        all_ids = []
                    
                    for book in books:
                        row=[]
                        for child in book.childNodes:
                          if(len(child.childNodes)!=0  and child.tagName != "id"):
                            row.append(child.firstChild.nodeValue)
#                            all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)                            
                self.latest_page+=1
#                self.pcs.copy_buffer()
 
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)   
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')           
         

    def _set_input_var(self,*args):
        
#        self.pcs._event.app.editor.error(str(type(args[0])))
        
        if str(args[-1])=="":
            self.get_search_input()
            
        self.search_input=str(args[-1])
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
#        self.book_repo=[]
        
#        pages=[i for i in range(1,32)]
#        
#        for page in pages:        
        try:
            
            data = requests.get(self.URL + "authortitle/" + search + "/page/"+str(page)+"/limit/25/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false

            if(data.status_code == 200):       
                try:
                    parsedData = minidom.parseString(data.text);
                except Exception as e:
#                    self.pcs._event.app.editor.error(str(e))
                    return
                    
                books = parsedData.getElementsByTagName('result')
                
                if(len(books) == 0):
#                        print("No books found")
                    pass
                else:
#                        all_ids = []
                    
                    for book in books:
                        row=[]
                        for child in book.childNodes:
                          if(len(child.childNodes)!=0  and child.tagName != "id"):
                            row.append(child.firstChild.nodeValue)
#                            all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row=row[::-1]
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)
                
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)  
                self.latest_page+=1 
                self.pcs.copy_buffer()                         
                    
 
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')          
         


    def get_book_id(self, id):
        # Search a particular book by ID
        page=self.latest_page
#        id=str(id)
        try:
            data = requests.get(self.URL + "id/" + str(id) + "/page/"+str(page)+"/limit/25/format/xml?API_key=" + self.KEY, verify=False)# during production remove verify = false
            if(data.status_code == 200):
                row=[]
                parsedData = minidom.parseString(data.text);
#                xml=parsedData.toxml('utf-8')

                try:                
                    msg = parsedData.getElementsByTagName('string')[0].firstChild.nodeValue
                    if msg=="No data existing":
                        self.pcs.menu_lvl="1-m"
                        self.pcs.show_msg(msg)
                except:
                    pass
                    
#                title = parsedData.getElementsByTagName('title')[0].firstChild.nodeValue
#                author = parsedData.getElementsByTagName('author')[0].firstChild.nodeValue
#                synopsis = parsedData.getElementsByTagName('brief-synopsis')[0]
#                row.append(title)
#                row.append(author)
#                
#                if(len(synopsis.childNodes) != 0):
#                    row.append(synopsis.firstChild.nodeValue) 
#                row.append(id)
#                
#                self.book_repo=[row]
#                self.pcs._event.app.editor.focus(self.WINDOW) 
##                os.system('clear')
#                self.pcs._event.current_window.buffer._files = self.book_repo
#                self.pcs._event.current_window.buffer.reset()
#                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
    
 
            else:
                
                self.pcs.menu_lvl="1-m"
                msg="id not found"
#                msg="Error, server replied with "+ str(data.status_code)
                self.pcs.show_msg(msg)
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    
            
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg="asdawe a af"+str(exc_tb.tb_lineno)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable')            
         
    def request_book_download(self, id):

        def send_request():
            page=self.latest_page
            try:
                authString = self.userid + ":"+self.password
    #            authString = "26353" + ':' +"9m85twwz"
                encoded = base64.b64encode(bytearray(authString.encode())).decode()
    #            print(id)
                headers = {'Authorization': 'Basic ' + encoded, "page" : str(page), "limit" : "1", "format" : "xml", "API_key" : self.KEY, "bookId" : id, "formatId" : '6'}
                data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/raiseBookDownloadRequest", headers = headers, verify=False)
     
    
                if(data.status_code == 200):
                    parsedData = minidom.parseString(data.text)
                    if parsedData.getElementsByTagName('message')!=[]:
                        message = parsedData.getElementsByTagName('message')[0]
                        self.pcs._event.app.editor.message("request sent")
#                        self.pcs._event.app.editor.message(str(id))
        #                self.pcs._event.app.editor.focus(self.WINDOW) 
                    else:
                        self.pcs._event.app.editor.message("Not available to download")
                else:
                    self.pcs.menu_lvl="1-e"
                    msg="Error, server replied with"+ str(data.status_code)
                    self.pcs.show_msg(msg)
            except Exception as e:
                self.userid=None
                self.pcs.menu_lvl="1-e"
                msg=str(e)#"Network unreachable"
                self.pcs.show_msg(msg)
        #            self.pcs._event.app.editor.error('Network is unreachable')           
             
        
        if self.login_status==False: 
            self.pcs.next_func=send_request
            self.pcs.login.login_process(self.pcs,self.pcs._event,"sp")
                            
        else:   
            send_request()
    


    def get_requested_books(self):
        # download books that are ready for downloading
#        self.pcs._event.current_window.buffer._files=[["invalid input"]]
#        self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)    
##        choice="1"
##        self.pcs.choice_selection(self.pcs._event, choice)

        def get_books():
            page=self.latest_page
            try:
                authString = self.userid + ":"+self.password
    #            authString = "26353" + ':' "9m85twwz"
                encoded = base64.b64encode(bytearray(authString.encode())).decode()
    #            print(id)
                headers = {'Authorization': 'Basic ' + encoded, "page" : str(page), "limit" : "10", "format" : "xml", "API_key" : self.KEY}
                data = requests.post("https://library.daisyindia.org/NALP/rest/NALPAPIService/fetchUserDownloadRequests", headers = headers, verify=False)
         
        
                if(data.status_code == 200):
                    parsedData = minidom.parseString(data.text)
    #                print(parsedData.toxml())
                    count = 1+(self.latest_page-1)*10
                    
                    books = parsedData.getElementsByTagName('result')
    #                t = PrettyTable(['ID', 'TITLE', 'STATUS'])
                    for book in books:
                        status = book.getElementsByTagName('available-to-download')[0].firstChild.nodeValue
                        row=[str(count), book.getElementsByTagName('title')[0].firstChild.nodeValue, status]
                        if(status == 'Available for Download'):
                            self.all_urls[str(count)] = book.getElementsByTagName('downloadUrl')[0].firstChild.nodeValue
                        count += 1
                        self.book_repo.append(row)
    #                print self.book_repo
                    self.menu_lvl="1-5"
    #                os.system('clear')
                    
                    self.pcs._event.current_window.buffer._files = self.book_repo
    #                self.pcs._event.app.editor.focus(self.WINDOW)
    #                os.system('clear')
    #                self.pcs._event.current_window.buffer.reset()
                    self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                    self.latest_page+=1
                    self.pcs.copy_buffer()
                    
      
                else:
                    self.pcs.menu_lvl="1-e"
                    msg="Error, server replied with"+ str(data.status_code)
                    self.pcs.show_msg(msg)
                
            except Exception as e:
                self.userid=None
                self.pcs.menu_lvl="1-e"
                msg=str(e)#"Network unreachable"
                self.pcs.show_msg(msg)
    #            self.pcs._event.app.editor.error('Network is unreachable')           
             
        if self.login_status==False: 
            self.pcs.next_func=get_books
            self.pcs.login.login_process(self.pcs,self.pcs._event,"sp")
                            
        else:   
            get_books()

    def download_book(self,response):
        

        def chdir(dir): 
            if directory_exists(dir) is False: 
#                os.makedirs(final_dir)
                ftp.mkd(dir)
            ftp.cwd(dir)
        
        def directory_exists(dir):
            filelist = []
            ftp.retrlines('LIST',filelist.append)
            for f in filelist:
                if f.split()[-1] == dir and f.upper().startswith('D'):
                    return True
            return False

        
        try:
#            final_dir=''
            import os
            current_dir= os.getcwd()
            final_dir= os.path.join(current_dir, str(download_folder))
#            if not os.path.exists(final_dir):
#               os.makedirs(final_dir)
               
            url = self.all_urls[response].split('/')
            host = url[2].split(':')[0]
            port = url[2].split(':')[1]
            filename = url[4]

 
            
            ftp = ftplib.FTP(host) 
            ftp.login(self.userid, self.password) 
            chdir(final_dir)
#            try:
#                ftp.cwd(final_dir)
#            except Exception as e:
#                self.pcs._event.app.editor.error('FTP dwD: '+str(e)[0:60])            

            ftp.retrbinary("RETR " + url[3] + "/" + url[4], open(filename, 'wb').write)
            
#            ftp.close()
            try:
                pass
#                ftp.quit()
            finally:
                self.pcs._event.app.editor.error('Download completed '+str(filename)[0:50])

                
        except KeyError:
            self.pcs._event.app.editor.error('queued')
 
#        except Exception as e:
#            self.pcs._event.app.editor.error('dwld: '+str(e)[0:50])
           
        except Exception as e:
            self.userid=None
            msg=str(e)#"Network unreachable"
#            self.pcs.show_msg(msg)
            self.pcs._event.app.editor.error(msg)           
         


    def get_book_categories(self):

#        self.book_repo=[]
        page=self.latest_page
        try:
            data = requests.get(self.URL + "categorylist/page/"+str(page)+"/limit/52/format/xml?API_key=" + self.KEY, verify=False) # during production remove verify = false
            if(data.status_code == 200):       
                parsedData = minidom.parseString(data.text);
                categories = parsedData.getElementsByTagName('title')
                
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
                self.pcs.copy_buffer()                           
                    
 
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)     
                
        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable') 


    def category_book_search(self, category_name):
        
#        self.book_repo=[]
        page=self.latest_page
        try:
            data = requests.get(self.URL + "category/" + category_name + "/page/"+str(page)+"/limit/52/format/xml?API_key=" + self.KEY, verify=False)
           
            if(data.status_code == 200):
                parsedData = minidom.parseString(data.text);
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
                        for child in book.childNodes:
                          if(len(child.childNodes)!=0  and child.tagName != "id"):
                            row.append(child.firstChild.nodeValue[:20])
#                            all_ids.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        row=row[::-1]
                        row.append(book.getElementsByTagName('id')[0].firstChild.nodeValue)
                        self.book_repo.append(row)

 
                self.pcs._event.app.editor.focus(self.WINDOW)        
                self.pcs._event.current_window.buffer._files = self.book_repo
                if page==1:
                    self.pcs._event.current_window.buffer.reset()
                self.pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                self.latest_page+=1
                self.pcs.menu_lvl="1-4-b"
                self.pcs.copy_buffer()
                                       
                    
 
            else:
                self.pcs.menu_lvl="1-e"
                msg="Error, server replied with"+ str(data.status_code)
                self.pcs.show_msg(msg)

        except Exception as e:
            self.userid=None
            self.pcs.menu_lvl="1-e"
            msg=str(e)#"Network unreachable"
            self.pcs.show_msg(msg)
#            self.pcs._event.app.editor.error('Network is unreachable') 
        
    def logout(self):
        choice="1"
        self.pcs.choice_selection(self.pcs._event, choice)
        if self.login_status==True:
            self.login_status=False
            self.userid=None
            self.password=None   
            self.pcs._event.app.editor.error('logged out of sugamya pustkalay')
        else:
            self.pcs._event.app.editor.error('already logged out')
            
