import sys
#sys.path.append('/home/cdh/vishal_iit/UIFramework')
#sys.path.append('/home/osboxes/Downloads/UIFramework')
#sys.path.append("/home/suman/vishal RBD/sugam_pustkalay/vishal_iit/UIFramework")
#sys.path.append("/tmp/guest-82o8ir/Downloads/sugam_pustkalay/sp-5july/NALP-master")
#sys.path.append("/home/rbd/RBC/sugam_pustkalay")
#sys.path.append("/home/rbd/RBC/sugam_pustkalay/vishal_iit/UIFramework")
#sys.path.append("/home/ubuntu/pustakalay")
sys.path.append("/home/suman/vishal RBD/sugam_pustkalay/pustakalay")
#sys.path.append("/home/suman/vishal RBD/sugam_pustkalay/vishal_iit/UIFramework")
import console
#import curses

from console.core.keybinding import Registry, MergedRegistry
from console.core.keys import Keys
from console.enums import DEFAULT_WINDOW
from console.core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType, SupportsRichText, IsBlockType, HasPropertyOn
from console.core.filters.base import OrFilter, AndFilter, NotFilter
from console.ui.window import EditorWindow
from console.ui.menu_window import Menu, MenuItem
from console.core.buffer_base import BufferBase

#------------------------------------------------------
from reader_buffer import ReaderBuffer
from login_buffer import LoginBuffer
from sugamya_pustakalya import SugamyaPustakalya as sp
from console.core.event_type import EventType
from _enums import BOOKLIST_WINDOW, LOGIN_WINDOW
from local_books import downloaded_files
from console.logger import logger
import traceback

class BookWindow(EditorWindow):
    pass


def load_custom_binding():
    _logger = logger('load_custom_binding')    
    try:    
        registry = Registry(EditorWindow)
        handle = registry.add_binding
    
        window_name ="MENU_LIST"
        from reader import process_choice_selection
        pcs=process_choice_selection(window_name)
    
        @handle(Keys.Home)
        def _(event):
            try:
                event.app.editor.focus(BOOKLIST_WINDOW)
                event.current_window.buffer._files=downloaded_files()
                event.current_window.buffer.reset()
                event.current_window.buffer.emit(EventType.TEXT_CHANGED)  
            except Exception as e:
                event.app.editor.error('unknown error %r' % e)
                
                
        @handle(Keys.ControlH)       
        def _(event):
            try:
                from login import _login
                pcs.sp=None
                pcs.bs=None
                pcs.login =_login()
            except:
                pass
            lst=[       
                        MenuItem('sugamya pustkalaya','s', lambda app: pcs.choice_selection(event,"1")),
                        MenuItem('bookshare','b', lambda app: pcs.choice_selection(event,"2")),
    #                    MenuItem('gutenberg','3', lambda app: pcs.choice_selection(event,"3")),
    #                    MenuItem('local books','4', lambda app: pcs.choice_selection(event,"4")),
                        MenuItem('quits','q', lambda app: pcs.choice_selection(event,"q")),
                            ]
            pcs.get_user_input(event.app,lst)
            
    #    @handle(Keys.Delete)
    #    def _(event):
    #        try:
    #            event.current_window.buffer.delete()
    #        except Exception as e:
    #            event.app.editor.error('unknown error %r' % e)
    
    #    @handle(Keys.Left)
    #    @handle(Keys.BackTab)    
    #    def _(event):
    #        try:
    #            if event.current_window.buffer._files==[]:
    #                event.app.editor.error('No book found')
    #            else:
    #                event.current_window.buffer.cursor_left()
    #        except Exception as e:
    #            event.app.editor.error('unable to navigate %r' % e)
    
    #    @handle(Keys.Right)
        @handle(' ')
        def _(event):
            try:
                event.app.editor.focus(BOOKLIST_WINDOW)
                if event.current_window.buffer._files==[]:
                    event.app.editor.error('No book found Space')
                else: 
                    event.current_window.buffer.cursor_right()
    
            except Exception as e:
                event.app.editor.error('unable to navigate %r' % e)
    
        @handle(Keys.Up)
        def _(event):
            try:
                handle=None
                if pcs.menu=="sp":
                    handle=pcs.sp
                elif pcs.menu=="bs":
                    handle=pcs.bs
                    
                event.app.editor.focus(BOOKLIST_WINDOW)
                
                buf=event.current_window.buffer
                lvl=buf.lvl
                
                if not handle==None and lvl==0 :
                    event.app.editor.error('start of list')
                    
                elif event.current_window.buffer._files==[]:
                    event.app.editor.error('No book found UP')
                else:
                    event.current_window.buffer.cursor_up()
            except Exception as e:
                event.app.editor.error('unable to navigate %r' % e)
    
        @handle(Keys.Down)
        def _(event):
            try:
                handle=None
                if pcs.menu=="sp":
                    handle=pcs.sp
                elif pcs.menu=="bs":
                    handle=pcs.bs
                    
                event.app.editor.focus(BOOKLIST_WINDOW)
                buf=event.current_window.buffer
                if buf._files==[]:
                    event.app.editor.error('No book found DOwn')
                
                lvl=buf.lvl
                if not handle==None and lvl==len(handle.book_repo)-1 and handle.total_books==str(len(handle.book_repo)):
                    event.app.editor.error('end of list')            
    
                elif not handle==None and lvl==len(handle.book_repo)-1:
                    if pcs.menu_lvl in ["1-4"]:
                        buf.cursor_down()
                    else:
                        event.app.editor.focus(BOOKLIST_WINDOW)
                        handle.pre_fetch_books()
                        buf._files =handle.book_repo
                        buf.lvl=lvl+1
                        buf.index=0
                        buf.emit(EventType.TEXT_CHANGED)
     
                    
                else:
                    buf.cursor_down()
            except Exception as e:
                event.app.editor.error('unable to navigate  %r ' % str(e)[0:50])
    
    
    
    
        def _search_book_id(*args):
            event=args[0]
            book_id=str(args[-1])
            if book_id=="" or ' ' in book_id :
                get_book_id_input(event)
            try:
                pcs.handle.get_book_id(book_id)
                pcs.menu_lvl="1-1-id"
            except IndexError:
                        event.app.editor.message('Book not Found id')
            except Exception as e:
                        event.app.editor.error(' %r ' % str(e)[0:60]) 
        
        def get_book_id_input(event):
            
            event.app.editor.input('search with id:',
                "PROMPT_WINDOW",
                on_ok_handler = _search_book_id)
    
    
    #    @handle(Keys.ControlF)
    #    def _(event):
    #        if pcs.menu=="sp":
    #            pcs.handle=pcs.sp
    #            choice="1"
    #        elif pcs.menu=="bs":
    #            pcs.handle=pcs.bs
    #            choice="2"
    #        if  not handle==None and pcs.menu_lvl in ["1-1"]:
    #            get_book_id_input(event)
    
            
        @handle(Keys.ControlR)
        def _(event):
            if  not pcs.sp==None and pcs.menu_lvl in ["1-1", "1-2", "1-3-b","1-4-b"]:
                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    lvl=pcs._event.current_window.buffer.lvl
                    book_id=pcs.sp.book_repo[lvl][-1].split("(")[0].strip().split(":")[-1].strip()#pcs.sp.book_repo[lvl][-1][3:]
#                    event.app.editor.error(' %r ' % book_id)
                    pcs.sp.request_book_download(book_id)
                except Exception as e:
                        event.app.editor.error(' %r ' % e) 
    
        @handle(Keys.PageUp)
        def _(event):
            handle=None
            if pcs.menu=="sp":
                handle=pcs.sp
            elif pcs.menu=="bs":
                handle=pcs.bs
            if  not handle==None and pcs.menu_lvl in ["1-1", "1-2", "1-3-b","1-4","1-4-b","1-5",]:
                event.app.editor.focus(BOOKLIST_WINDOW)
                pcs._event.current_window.buffer.reset()
    
        @handle(Keys.PageDown)
        def _(event):
            handle=None
            if pcs.menu=="sp":
                handle=pcs.sp
            elif pcs.menu=="bs":
                handle=pcs.bs
                
            if  not handle==None and pcs.menu_lvl in ["1-1", "1-2", "1-3-b","1-4","1-4-b","1-5"]:
                event.app.editor.focus(BOOKLIST_WINDOW)
                pcs._event.current_window.buffer.index=0
                pcs._event.current_window.buffer.lvl=len(handle.book_repo)-1
                pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
     
    #            pcs._event.current_window.buffer.bottom()

    
        @handle(Keys.Backspace)
        def _(event):
            handle=None
             
            if pcs.menu=="sp":
                handle=pcs.sp
                choice="1"
            elif pcs.menu=="bs":
                handle=pcs.bs
                choice="2"
            if  not handle==None and pcs.menu_lvl in ["1","2","1-1", "1-2", "1-3","1-3-b","1-3-e", "1-4", "1-4-b", "1-5","1-m","1-e"]:
                if pcs.menu_lvl in ["1-m","1-4-b"]:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    pcs._event.current_window.buffer.go_to_prev_state()
                    pcs.menu_lvl=pcs.prev_menu_lvl
                    handle.book_repo=pcs._event.current_window.buffer._files
                    handle.total_books=pcs._event.current_window.buffer.prev_total_books
                    
                if pcs.menu_lvl in ["1-3-e","1-3-b"]:
                    pcs.menu_lvl=="1-3"
                    pcs._event.current_window.buffer.reset()
                    pcs.get_user_input(event.app,pcs.search_menu_lst)
                    
                else:
                    try:
                        event.app.editor.focus(BOOKLIST_WINDOW)
                        pcs._event.current_window.buffer._files=downloaded_files()
                        pcs._event.current_window.buffer.reset()
                        pcs.choice_selection(event, choice)
                    except Exception as e:
                            event.app.editor.error(' %r ' % e) 
 
   
    
        @handle(Keys.ControlD)
        def _(event):
            if pcs.menu=="sp" and pcs.menu_lvl in ["1-5"]:
                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    lvl=pcs._event.current_window.buffer.lvl
                    book_id=pcs.sp.book_repo[lvl][-1].split("(")[0].strip().split(":")[-1].strip()#pcs.sp.book_repo[lvl][-1][3:]
                    event.app.editor.message('downloading...')
                    import threading
                    t=threading.Thread(target=pcs.sp.download_book, args=(book_id,))
                    t.start()
                    pcs.sp.download_threads.append(t)
                except Exception as e:
                    event.app.editor.error(' %r ' % str(e)[0:60])
                        
            if pcs.menu=="bs" and pcs.menu_lvl in ["1-1", "1-2", "1-3-b", "1-4-b","1-m"]:
                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    lvl=pcs._event.current_window.buffer.lvl
#                    repo=pcs._event.current_window.buffer._files[-1]
#                    book_id=pcs.remove_book_index([repo])[-1][-1]
                    book_id=pcs.bs.book_repo[lvl][-1].split("(")[0].strip().split(":")[-1].strip()#pcs.sp.book_repo[lvl][-1][3:]
    #                event.app.editor.message('downloading...')
                    pcs.bs.book_download(book_id)
    #                import threading
    #                t_bs=threading.Thread(target=pcs.bs.book_download, args=(book_id,))
    #                t_bs.start()
    #                pcs.bs.download_threads.append(t)
                except Exception as e:
                    event.app.editor.error(' %r ' % str(e)[0:60])
    
                        
        @handle(Keys.Enter)
        def _(event):
            handle=None
            if pcs.menu=="sp":
                handle=pcs.sp
                choice="1"
            elif pcs.menu=="bs":
                handle=pcs.bs
                choice="2" 
    
    
            if  not handle==None and pcs.menu_lvl in ["1-4"]:
                handle.c_page_index=1
                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
#                    handle.book_repo_temp=handle.book_repo
                    lvl=pcs._event.current_window.buffer.lvl
                    handle.category_name=handle.book_repo[lvl][-1].split("(")[0].strip()
                    handle.book_repo=[] 
                    handle.c_book_repo=[]
#                    pcs._event.current_window.buffer.reset()
                    handle.category_book_search(handle.category_name)
                except Exception as e:
                        event.app.editor.error(' %r ' % e) 

            if pcs.menu_lvl in ["1-3-e"]:
                pcs.menu_lvl=="1-3"
                pcs.get_user_input(event.app,pcs.search_menu_lst)
    
    
            if  not handle==None and pcs.menu_lvl in ["1-e"]:
    #            from local_books import downloaded_files


                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    pcs._event.current_window.buffer._files=downloaded_files()
                    pcs._event.current_window.buffer.reset()
                    pcs.choice_selection(event, choice)
                except Exception as e:
                        event.app.editor.error(' %r ' % e)
    
            if not handle==None and pcs.menu_lvl in ["1-m"]:
    #            from local_books import downloaded_files
                try:
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    pcs._event.current_window.buffer.go_to_prev_state()
                    pcs.menu_lvl=pcs.prev_menu_lvl
    ##                pcs._event.current_window.buffer._files= downloaded_files()
    ##                pcs._event.current_window.buffer.reset()
    #                pcs.choice_selection(event, choice)
                except Exception as e:
                        event.app.editor.error(' %r ' % str(e)[0:60])
            if handle == None:
                try:
                    import os
                    current_directory = os.getcwd()
                    _dir= os.path.join(current_directory, r'Downloads')
                    event.app.editor.focus(BOOKLIST_WINDOW)
                    lvl=event.current_window.buffer.lvl
                    f=event.current_window.buffer._files[lvl][0]                        
                    path=os.path.join(_dir, f)
                    event.current_window.buffer.enter(path)
                except Exception as e:
                    event.app.editor.error(' %r ' % str(e)[0:60])
        return registry
    
    except:
        _logger.error('application exited with exception: %r' % traceback.format_exc())
        raise
    finally:
        pass



def main(stdscr, args):
    
    top, left = stdscr.getbegyx() # top left coordinate of the screen
    rows, cols = stdscr.getmaxyx() # size of screen

    console.init(stdscr)

    from console.logger import logger

    _logger = logger('main')


    try:
        from os import path
        import traceback
        from console.application import Application
        from console.ui.editor import Editor
        from console.ui.window import Window,EditorWindow,PromptWindow
        from console.enums import DEFAULT_WINDOW
        from console.config import PROMPT_HEIGHT
        from console.core.prompt_buffer import PromptBuffer
#        from binding import load_custom_binding
        
        
        _logger.debug('terminal size %dx%d' % (rows, cols))

#--------------------------------------------------

        book_buffer = ReaderBuffer()
        book_buffer.is_readonly = False
        
        
        booklistwindow = EditorWindow(name = BOOKLIST_WINDOW,
                top = top,
                left = left,
                rows = rows - PROMPT_HEIGHT,
                columns = cols,
                buf = book_buffer,
                wrap = True)         

#--------------------------------------------------

        login_buffer = LoginBuffer()
        login_buffer.is_readonly = False
        
        
        loginwindow = EditorWindow(name = LOGIN_WINDOW,
                top = top,
                left = left,
                rows = rows - PROMPT_HEIGHT,
                columns = cols,
                buf = book_buffer,
                wrap = True) 

#---------------------------------------------------
 
        edit_buffer = PromptBuffer()
        edit_buffer.is_readonly = False


        editwindow = EditorWindow(name = DEFAULT_WINDOW,
                top = top,
                left = left,
                rows = rows - PROMPT_HEIGHT,
                columns = cols,
                buf = edit_buffer,
                wrap = False)


        
        editor = Editor(
                        rows - PROMPT_HEIGHT, 	# editable area height
                        cols,			# editable area width
                        rows - PROMPT_HEIGHT,	# prompt row
                        PROMPT_HEIGHT,		# height of prompt window(1)
                        cols,
                        windows = [editwindow,booklistwindow,loginwindow ],#
                        initial_focused_window = BOOKLIST_WINDOW)#BOOKLIST_WINDOW )


        registry = MergedRegistry([
            console.default_bindings(),
            load_custom_binding()
            ])

        app = Application(editor, registry = registry)
        app.run()
        
        
    except:
        _logger.error('application exited with exception: %r' % traceback.format_exc())
        raise
    finally:
        pass


console.run(main, sys.argv)

