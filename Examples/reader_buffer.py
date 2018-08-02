from __future__ import unicode_literals

from console.logger import logger
from console.core.event_type import EventType
from console.core.buffer_base import BufferBase

#---------
from local_books import downloaded_files
from console.logger import logger
#from sugamya_pustakalya import SugamyaPustakalya as sp


class ReaderBuffer(BufferBase):
    _logger = logger('reader-buffer') 

    def __init__(self, name = '', text ='' ):
        BufferBase.__init__(self, name)
        
        self._text = text
        
#        _files=downloaded_files()
#        if _files==[]:
#            self._files=[["No Books in Download"]]
#        else:
#            self._files = _files
        
        self._files=downloaded_files()
        self.prev_files=[]        
        self.lvl=0
        self.prev_lvl=0
        self.index=0
        self.prev_index=0 

    @property
    def text(self):
        return self._files[self.lvl][self.index]

    @text.setter
    def text(self, value):
        self._text = value
        self.emit(EventType.TEXT_CHANGED)

    def cursor_right(self):
        self.index+=1
        if self.index > len(self._files[self.lvl])-1:
#            self.index=len(self._files[self.lvl])-1
            self.index=0    #circular movement
            
        self.emit(EventType.TEXT_CHANGED)
        
    def cursor_left(self):
        self.index-=1
        if self.index < 0:
#            self.index=0
            self.index=len(self._files[self.lvl])-1     #circular movement
            
        self.emit(EventType.TEXT_CHANGED)
    
    def cursor_up(self):
        self.index=0
        self.lvl-=1
        if self.lvl < 0:
            self.lvl = 0
#            self.lvl=len(self._files)-1    #circular movement
            
        self.emit(EventType.TEXT_CHANGED)


    def cursor_down(self):
        self.index=0
        self.lvl+=1


        
        if self.lvl > len(self._files)-1:
                self.lvl = len(self._files)-1
    #            self.lvl=0     #circular movement

#        if pcs.menu_lvl=="11" and sp.latest_page>1:
#            self.lvl = len(self._files)
#            sp.get_latest_books()  

           
        self.emit(EventType.TEXT_CHANGED)
        

    @property
    def is_readonly(self):
        return self._readonly_document


    @is_readonly.setter
    def is_readonly(self, value):
        self._readonly_document = value

    def top(self):
        pass

    def bottom(self):
        pass

    def reset(self):
        self.index=0
        self.lvl=0
        try:
            self.emit(EventType.TEXT_CHANGED)
        except:
            pass
        
    def enter(self):
        _logger = logger('reader_buffer')
        _logger.error('  opening selected file...')
        
    def delete(self):
        _logger = logger('reader_buffer')
        _logger.error('  deleting file...')
        
    def go_to_prev_state(self):
        self.index=self.prev_index
        self.lvl=self.prev_lvl
        self._files=self.prev_files
        self.emit(EventType.TEXT_CHANGED)

