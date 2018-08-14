# uncompyle6 version 3.1.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 (default, Nov 23 2017, 15:37:09) 
# [GCC 6.3.0 20170406]
# Embedded file name: /home/osboxes/Downloads/UIFramework/examples/reader.py
# Compiled at: 2018-04-24 12:27:42
from console.ui.menu_window import Menu, MenuItem
from sugamya_pustakalya import SugamyaPustakalya
from bookshare import Bookshare
from console.core.event_type import EventType
from _enums import BOOKLIST_WINDOW, LOGIN_WINDOW,DEFAULT_WINDOW

#-------------
from login import _login
from local_books import downloaded_files


class process_choice_selection():

    def __init__(self, window_name=None):
        self._event = None
        self.window_name = window_name
        self.reader_menu_lst = None
        self.lvl = 0
        self.menu_lvl=""
        self.sp=None
        self.bs=None
        self.login_lvl=""
        self.login =_login()
        self.count=0
        self.menu=""
        self.next_func=None



    def choice_selection(self, _event, choice):
        self._event=_event
        app=_event.app
        
        choice = str(choice)
        if choice == '1':
            
            if self.sp==None:
                self.sp = SugamyaPustakalya(self)
#                
#                if not self.login.login_lvl=="sp":
#                    self.login.login_process(self,_event,"sp")
 
#            else:
            self.menu="sp"
            self.menu_lvl="1"
            lst = [
                     MenuItem('Latest books', '1', lambda app: self.sp_choice_selection(app, '1')),
                     MenuItem('Popular books', '2', lambda app: self.sp_choice_selection(app, '2')),
                     MenuItem('Search Books', '3', lambda app: self.sp_choice_selection(app, '3')),
                     MenuItem('Book Categories', '4', lambda app: self.sp_choice_selection(app, '4')),
                     MenuItem('Downloads', '5', lambda app: self.sp_choice_selection(app, '5')),
                     MenuItem('Logout', '6', lambda app: self.sp_choice_selection(app, '6')),
                     MenuItem('Go Back', 'b', lambda app: self.sp_choice_selection(app, 'b')),
                     MenuItem('quits', 'q', lambda app: self.sp_choice_selection(app, 'q'))
                 ]
    
            
#                if  self.login.login_lvl=="sp":
            self.get_user_input(app,lst)
 
#                else:
#                    app.editor.message( 'ELSE,READER in sp: ' )
        
        elif choice == '2':
            if self.bs==None:
                self.bs = Bookshare(self)
#                if not self.login.login_lvl=="bs":
#                    self.login.login_process(self,_event,"bs")  

#            else:
            self.menu="bs"
            self.menu_lvl="1"
            lst = [
                     MenuItem('Latest books', '1', lambda app: self.bs_choice_selection(app, '1')),
                     MenuItem('Popular books', '2', lambda app: self.bs_choice_selection(app, '2')),
                     MenuItem('Search Books', '3', lambda app: self.bs_choice_selection(app, '3')),
                     MenuItem('Book Categories', '4', lambda app: self.bs_choice_selection(app, '4')),
#                     MenuItem('Downloads', '5', lambda app: self.bs_choice_selection(app, '5')),
                     MenuItem('Logout', '6', lambda app: self.bs_choice_selection(app, '6')),
                     MenuItem('Go Back', 'b', lambda app: self.bs_choice_selection(app, 'b')),
                     MenuItem('quits', 'q', lambda app: self.bs_choice_selection(app, 'q'))
                 ]
    
#            if  self.login.login_lvl=="bs":
            self.get_user_input(app,lst)

#            else:
#                app.editor.message( 'ELSE READER in bs menu: ' )                    
                    
                
        elif choice == '3':
            self.menu_lvl="3"
            app.editor.message('gutenberg ')
        elif choice == '4':
            self.menu_lvl="4"
            app.editor.message('local books ')
        elif choice == 'q':
            def _on_yes(e):
                self.menu_lvl="1"
                try:
                    self.sp=None
                    self.bs=None
                    self.login =_login()
    #                self._event.current_window.buffer._files=[[""]]
                    self._event.current_window.buffer.reset()
    #                self._event.current_window.buffer._files=downloaded_files()
                    self.sp.logout()
                except:
                    pass
     
                try:
                    self.bs.logout()
                except:
                    pass
                
            def _on_no(e):
                self.get_user_input( app,self.reader_menu_lst)
    
            app.editor.confirm('confirm quit?(y/n)', on_yes_handler = _on_yes, on_no_handler = _on_no)            
        else:
            app.editor.message('\nInvalid choice.\n ')

    def bs_choice_selection(self, app, choice):
        if choice == '1':
            self.menu_lvl="1-1"
            self.bs.book_repo=[]
            self.bs.latest_page=1
            self.bs.get_latest_books()
            
        elif choice == '2':
            self.menu_lvl="1-2"
            self.bs.book_repo=[]
            self.bs.latest_page=1
            self.bs.get_popular_books()
            
        elif choice == '3':
            self.menu_lvl="1-3"
            self.bs.book_repo=[]
            self.bs.latest_page=1
            self.bs.get_search_input()
            
        elif choice == '4':
            self.menu_lvl="1-4"
            self.bs.book_repo=[]
            self.bs.latest_page=1
            self.bs.get_book_categories()
            
        elif choice == '5':
            self.menu_lvl="1-5"
            self.bs.book_repo=[]
            self.bs.latest_page=1
            self.all_urls = {}
            self.bs.get_requested_books()
            
        elif choice == '6':
            
            def _on_yes(e):
                self.bs.logout()
            def _on_no(e):
                choice="2" 
                self.choice_selection(self._event, choice)            
            
            app.editor.confirm('confirm logout?(y/n)', on_yes_handler = _on_yes, on_no_handler = _on_no)            
                        
        elif choice == 'b':
            self.menu_lvl="1"
            self.get_user_input( app,self.reader_menu_lst)
            
        elif choice == 'q':
            def _on_yes(e):
                self.menu_lvl="1"
                try:
                    self.bs=None
                    self.login =_login()
    #                self._event.current_window.buffer._files=[[""]]
                    self._event.current_window.buffer.reset()
    #                self._event.current_window.buffer._files=downloaded_files()
                    self.bs.logout()
                except:
                    pass
    
            def _on_no(e):
                    choice="2" 
                    self.choice_selection(self._event, choice)      
    
            app.editor.confirm('confirm quit?(y/n)', on_yes_handler = _on_yes, on_no_handler = _on_no)
            
        else:
            app.editor.message('\nInvalid choice.\n ')


    def sp_choice_selection(self, app, choice):
        if choice == '1':
            self.menu_lvl="1-1"
#            self.sp = SugamyaPustakalya(self)
#            app.editor.message("fetching books...")
            self.sp.book_repo=[]
            self.sp.latest_page=1
            self.sp.get_latest_books()
            
        elif choice == '2':
            self.menu_lvl="1-2"
#            app.editor.message('Popular books ')
            self.sp.book_repo=[]
            self.sp.latest_page=1
            self.sp.get_popular_books()
            
        elif choice == '3':
            self.menu_lvl="1-3"
#            app.editor.message('Search Books')
            self.sp.book_repo=[]
            self.sp.latest_page=1
            self.sp.get_search_input()
            
        elif choice == '4':
            self.menu_lvl="1-4"
#            app.editor.message('Book Categories')
            self.sp.book_repo=[]
            self.sp.latest_page=1
            self.sp.get_book_categories()
            
        elif choice == '5':
            self.menu_lvl="1-5"
#            app.editor.message('Downloads ')
            self.sp.book_repo=[]
            self.sp.latest_page=1
            self.all_urls = {}
            self.sp.get_requested_books()
            
        elif choice == '6':
            
            def _on_yes(e):
                self.sp.logout()
                
            def _on_no(e):
                choice="1" 
                self.choice_selection(self._event, choice)            
            
            app.editor.confirm('confirm logout?(y/n)', on_yes_handler = _on_yes, on_no_handler = _on_no)            
            
        elif choice == 'b':
            self.menu_lvl="1"
    #                                    app.editor.message('Go Back ')
            self.get_user_input( app,self.reader_menu_lst)
        elif choice == 'q':
            def _on_yes(e):
                self.menu_lvl="1"
                try:
                    self.sp=None
                    self.login =_login()
                    self._event.current_window.buffer.reset()
                    self.sp.logout()
                except:
                    pass
            def _on_no(e):
                    choice="1" 
                    self.choice_selection(self._event, choice)
    
            app.editor.confirm('confirm quit?(y/n)', on_yes_handler = _on_yes, on_no_handler = _on_no)
 
        else:
            app.editor.message('\nInvalid choice.\n ')

    def copy_buffer(self):
        buf=self._event.current_window.buffer
        buf.prev_lvl=buf.lvl
        buf.prev_index=buf.index
        buf.prev_files=buf._files


    def get_user_input(self, app,lst):
        if self.lvl == 0:
            self.reader_menu_lst = lst
            self.lvl += 1

        app.editor.create_menu(self.window_name,lst)

