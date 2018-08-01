#"26353" "9m85twwz"

from console.ui.menu_window import Menu, MenuItem
from sugamya_pustakalya import SugamyaPustakalya
from bookshare import Bookshare
from console.core.event_type import EventType
from _enums import BOOKLIST_WINDOW, LOGIN_WINDOW,DEFAULT_WINDOW

class _login():
    def __init__(self):
        self.userid=None
        self.password=None      
        self.login_lvl=None
        self.event=None
        self.pcs=None
        self.login_status=0
        self.login_tag=""


    def _on_password_ok(self,*args):
 
        self.password=str(args[-1])
#            self.event.app.editor.error(str(self.pcs.sp.check_credentials(self.userid,self.password)))
        if self.login_tag=="sp":
            self.password="9m85twwz"
            handle=self.pcs.sp 
            choice="1"
            response=handle.check_credentials(self.userid,self.password)
            if response==1:
                self.login_status=1
                self.login_lvl=self.login_tag
                handle.login_status=True
                self.pcs.next_func()
                
            else:
                if self.pcs.menu_lvl in ["1-5"]:
                    self.pcs.choice_selection( self.event, choice)
                self.event.app.editor.error(str(response))
                
#        if self.login_tag=="bs":
#            self.password="vis2alll"
#            handle=self.pcs.bs  
#            choice="2" 
               
 
    def get_password(self):
        self.event.app.editor.input('password:',
                    "PROMPT_WINDOW",
                    on_ok_handler = self._on_password_ok)
    
    def _on_userid_ok(self,*args):
        self.userid = str(args[-1])
        self.userid="26353"
        self.get_password()

        

        
    def login_process(self,pcs,event,login_tag):
        self.login_status=0
        self.login_tag=login_tag
        self.pcs=pcs
        self.event=event
        event.app.editor.input('userid:',
                "PROMPT_WINDOW",
                on_ok_handler = self._on_userid_ok)     

 

            