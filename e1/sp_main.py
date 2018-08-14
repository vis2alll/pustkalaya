import sys
#sys.path.append('/home/cdh/vishal_iit/UIFramework')
#sys.path.append('/home/osboxes/Downloads/UIFramework')
#sys.path.append("/home/suman/vishal RBD/sugam_pustkalay/vishal_iit/UIFramework")
#sys.path.append("/tmp/guest-82o8ir/Downloads/sugam_pustkalay/sp-5july/NALP-master")
#sys.path.append("/home/rbd/RBC/sugam_pustkalay")
#sys.path.append("/home/rbd/RBC/sugam_pustkalay/vishal_iit/UIFramework")
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

class BookWindow(EditorWindow):
    pass
 

def load_custom_binding():
    registry = Registry(EditorWindow)
    handle = registry.add_binding

    window_name ="MENU_LIST"
    from reader import process_choice_selection
    pcs=process_choice_selection(window_name)

    @handle(Keys.AltM)
    def _(e):
        # current_window = e.current_window
        # current_window = e.app.editor.current_window

        e.app.editor.message('message demo')

    @handle(Keys.AltE)
    def _(e):
        e.app.editor.error('error message demo')

    @handle(Keys.AltC)
    def _(e):
        def _on_yes(e):
            e.app.editor.message('you pressed yes')

        def _on_no(e):
            e.app.editor.message('you pressed no')

        e.app.editor.confirm('confirm?', on_yes_handler = _on_yes, on_no_handler = _on_no)

    def search_from_top():
        print "pass as d;lf"

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
                    MenuItem('sugamya pustkalaya','1', lambda app: pcs.choice_selection(event,"1")),
                    MenuItem('bookshare','2', lambda app: pcs.choice_selection(event,"2")),
                    MenuItem('gutenberg','3', lambda app: pcs.choice_selection(event,"3")),
                    MenuItem('local books','4', lambda app: pcs.choice_selection(event,"4")),
                    MenuItem('quits','q', lambda app: pcs.choice_selection(event,"q")),
                        ]
        pcs.get_user_input(event.app,lst)
        
    @handle(Keys.Delete)
    def _(event):
        try:
            event.current_window.buffer.delete()
        except Exception as e:
            event.app.editor.error('unknown error %r' % e)

    @handle(Keys.Left)
    def _(event):
        try:
            if event.current_window.buffer._files==[]:
                event.app.editor.error('No book found')
            else:
                event.current_window.buffer.cursor_left()
        except Exception as e:
            event.app.editor.error('unable to navigate %r' % e)

    @handle(Keys.Right)
    def _(event):
        try:
            if event.current_window.buffer._files==[]:
                event.app.editor.error('No book found')
            else: 
                event.current_window.buffer.cursor_right()

        except Exception as e:
            event.app.editor.error('unable to navigate %r' % e)

    @handle(Keys.Up)
    def _(event):
        try:
            if event.current_window.buffer._files==[]:
                event.app.editor.error('No book found')
            else:
                event.current_window.buffer.cursor_up()
        except Exception as e:
            event.app.editor.error('unable to navigate %r' % e)

    @handle(Keys.Down)
    def _(event):
        try:
            if event.current_window.buffer._files==[]:
                event.app.editor.error('No book found')
            else:
                event.current_window.buffer.cursor_down()
        except Exception as e:
            event.app.editor.error('unable to navigate  %r ' % e)

    def _search_book_id(*args):
        event=args[0]
        book_id=str(args[-1])
        if book_id=="" or ' ' in book_id :
            get_book_id(event)
        try:
            pcs.sp.get_book_id(book_id)
            pcs.menu_lvl="1-1-id"
        except IndexError:
                    event.app.editor.message('Book not Found')
        except Exception as e:
                    event.app.editor.error(' %r ' % str(e)[0:60]) 
    
    def get_book_id(event):
        event.app.editor.input('search input:',
            "PROMPT_WINDOW",
            on_ok_handler = _search_book_id)


    @handle(Keys.ControlF)
    def _(event):
        if  not pcs.sp==None and pcs.menu_lvl=="1-1":
            get_book_id(event)
        
        
    @handle(Keys.ControlR)
    def _(event):
        if  not pcs.sp==None and pcs.menu_lvl in ["1-1", "1-2", "1-3","1-4-b"]:
            try:
                lvl=pcs._event.current_window.buffer.lvl
                book_id=pcs.sp.book_repo[lvl][-1]
                pcs.sp.request_book_download(book_id)
            except Exception as e:
                    event.app.editor.error(' %r ' % e) 

    @handle(Keys.ControlB)
    def _(event):
        handle=None
        if pcs.menu=="sp":
            handle=pcs.sp
            choice="1"
        elif pcs.menu=="bs":
            handle=pcs.bs
            choice="2"
        if  not handle==None and pcs.menu_lvl in ["1-1", "1-2", "1-3", "1-4", "1-4-b", "1-5","1-m"]:
            if pcs.menu_lvl=="1-m":
                pcs._event.current_window.buffer.go_to_prev_state()
            else:
                from local_books import downloaded_files
                try:
                    pcs._event.current_window.buffer._files=downloaded_files()
                    pcs._event.current_window.buffer.reset()
                    pcs.choice_selection(event, choice)
                except Exception as e:
                        event.app.editor.error(' %r ' % e) 

    @handle(Keys.ControlN)
    def _(event):
        handle=None
        if pcs.menu=="sp":
            handle=pcs.sp
        elif pcs.menu=="bs":
            handle=pcs.bs            
        if  not handle==None and pcs.menu_lvl in ["1-1", "1-2", "1-3", "1-4", "1-4-b","1-5"]:
            try:
                lvl=len(handle.book_repo)

                if pcs.menu_lvl=="1-1":
                    handle.get_latest_books()
                elif pcs.menu_lvl=="1-2":
                    handle.get_popular_books()
                elif pcs.menu_lvl=="1-3":
                    handle.search_book()
                elif pcs.menu_lvl=="1-4":
                    if handle==pcs.bs:
                        pass
                    else:
                        handle.get_book_categories()
                elif pcs.menu_lvl=="1-4-b":
                    handle.category_book_search( handle.category_name)
                elif pcs.menu_lvl=="1-5":
                    handle.get_requested_books()
                try:
                    repo_length=len(handle.book_repo)
                    if not lvl==repo_length:
                        pcs._event.current_window.buffer.lvl=lvl
                        pcs._event.current_window.buffer.index=0
                        pcs._event.current_window.buffer.emit(EventType.TEXT_CHANGED)
                except:
                    pass
            except Exception as e:
                    event.app.editor.error(' %r  ' % e) 


 

    @handle(Keys.ControlD)
    def _(event):
        if pcs.menu=="sp" and pcs.menu_lvl in ["1-5"]:
            try:
                lvl=pcs._event.current_window.buffer.lvl
                book_id=pcs.sp.book_repo[lvl][0]
                event.app.editor.message('downloading...')
                import threading
                t=threading.Thread(target=pcs.sp.download_book, args=(book_id,))
                t.start()
                pcs.sp.download_threads.append(t)
            except Exception as e:
                event.app.editor.error(' %r ' % e) 
                    
        if pcs.menu=="bs" and pcs.menu_lvl in ["1-1", "1-2", "1-3-b", "1-4-b"]:
 
            try:
                lvl=pcs._event.current_window.buffer.lvl
                book_id=pcs.bs.book_repo[lvl][-1]
#                event.app.editor.message('downloading...')
                import threading
                t=threading.Thread(target=pcs.bs.book_download, args=(book_id,))
                t.start()
                pcs.bs.download_threads.append(t)
            except Exception as e:
                event.app.editor.error(' %r ' % e)

                    
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
            handle.latest_page=1
            try:
                handle.book_repo_temp=handle.book_repo
                lvl=pcs._event.current_window.buffer.lvl
                handle.category_name=handle.book_repo[lvl][-1]
                handle.book_repo=[] 
                handle.category_book_search(handle.category_name)
            except Exception as e:
                    event.app.editor.error(' %r ' % e) 

        if not handle==None and pcs.menu_lvl in ["1-m"]:
#            from local_books import downloaded_files
            try:
                pcs._event.current_window.buffer.go_to_prev_state()
##                pcs._event.current_window.buffer._files= downloaded_files()
##                pcs._event.current_window.buffer.reset()
#                pcs.choice_selection(event, choice)
            except Exception as e:
                    event.app.editor.error(' %r ' % str(e)[0:60])
        else:
            try:
                event.current_window.buffer.enter()
            except Exception as e:
                event.app.editor.error('unknown error %r' % e)
                
    return registry




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

