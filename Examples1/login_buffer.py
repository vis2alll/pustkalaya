from __future__ import unicode_literals

from console.logger import logger
from console.core.event_type import EventType
from console.core.buffer_base import BufferBase

#---------
from local_books import downloaded_files
from console.logger import logger
#from sugamya_pustakalya import SugamyaPustakalya as sp


class LoginBuffer(BufferBase):
    _logger = logger('login-buffer') 

    def __init__(self, name = '' ,text=""):
        BufferBase.__init__(self, name)
        self._text = text
                
        self.userid=""
        self.password=""
        
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.emit(EventType.TEXT_CHANGED)

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value

        if self._cursor >= len(self.text):
            if self.is_readonly:
                self._cursor = max(len(self.text) - 1, 0)
            else:
                self._cursor = len(self.text)
        if self._cursor < 0:
            self._cursor = 0

        self.emit(EventType.CURSOR_MOVED)

    @property
    def is_readonly(self):
        return self._readonly_document


    @is_readonly.setter
    def is_readonly(self, value):
        self._readonly_document = value

    @property
    def selection_range(self):
        return None

    @property
    def format_ranges (self):
        return []

    def insert_text(self, ch):
        if self.is_readonly:
            BufferBase._logger.debug('buffer is readonly')
            return

        text = chr(ch)
        if len(self.text) == 0:
            self._text = text
        else:
            first = u''
            last = u''

            if self._cursor > 0:
                first = self.text[:self._cursor]

            if self._cursor <= len(self.text):
                last = self.text[self._cursor:]

            self._text = first + text + last

        self._cursor += 1
        self.emit(EventType.TEXT_CHANGED)

    def remove(self, count = -1):
        if self.is_readonly:
            BufferBase._logger.debug('buffer is readonly')
            return

        # nothing to delete
        if (len(self.text) == 0 or
                (self.cursor == 0 and count < 0) or
                (self.cursor == len(self.text) and count > 0)):
                return

        first = u''
        last = u''

        if count < 0: # backspace
            count = -count
            first = self.text[:self._cursor - count]
            if self._cursor < len(self.text):
                last = self.text[self._cursor:]

            self._cursor -= count
        else: # delete
            last = self.text[self._cursor + count:]
            if self._cursor > 0:
                first = self.text[:self._cursor]

        self._text = first + last

        self.emit(EventType.TEXT_CHANGED)

    def enter(self):
        pass

    def cursor_up(self, rows = 1):
        pass

    def cursor_down(self, rows = 1):
        pass

    def cursor_left(self, cols = 1):
        self.cursor = self.cursor - cols

    def cursor_right(self, cols = 1):
        self.cursor = self.cursor + cols

    def cursor_beg(self):
        self.cursor = 0

    def cursor_end(self):
        self.cursor = len(self.text)

    def top(self):
        pass

    def bottom(self):
        pass

    def previous(self, blocktype):
        return None

    def next(self, blocktype):
        return None

    def delete(self):
        pass

    # search and replace
    def reset_search(self):
        self._new_search = True
        self._search_text = None

    def search(self, search_text, back_search):
        raise NotImplementedError

    def _find_match(self, back_search):
        raise NotImplementedError


    def next_match(self, search_text, back_search, from_top = False):
        return None

    def replace(self, search_text, replace_text, back_search):
        return None

    def replace_all(self, search_text, replace_text, back_search):
        return None

    # clipboard
    def clipboard_copy(self):
        self.toggle_property(BufferBase.PROPERTY_SELECTION, reset = False)
        BufferBase._logger.info('clipboard_copy not implemented')

    def clipboard_cut(self):
        self.toggle_property(BufferBase.PROPERTY_SELECTION, reset = False)
        BufferBase._logger.info('clipboard_cut not implemented')

    def clipboard_paste(self):
        BufferBase._logger.info('clipboard_paste not implemented')

    def clipboard_delete(self):
        self.toggle_property(BufferBase.PROPERTY_SELECTION, reset = False)
        BufferBase._logger.info('clipboard_delete not implemented')

    def toggle_property(self, prop, **args):
        if prop == BufferBase.PROPERTY_READONLY:
            self._readonly_document = not self._readonly_document
            self.focus()
        elif prop == BufferBase.PROPERTY_BOLD:
            self._bold_forced_on = not self._bold_on
            self._bold_on = self._bold_forced_on
        elif prop == BufferBase.PROPERTY_ITALIC:
            self._italic_forced_on = not self._italic_on
            self._italic_on = self._italic_forced_on
        elif prop == BufferBase.PROPERTY_UNDERLINE:
            self._underline_forced_on = not self._underline_on
            self._underline_on = self._underline_forced_on
        elif prop == BufferBase.PROPERTY_SELECTION:
            if self._selection_on:
                reset = args.pop('reset', True)
                self.emit(EventType.TEXT_CHANGED)
            else:
                self.emit(EventType.TEXT_CHANGED)
            self._selection_on = not self._selection_on
        else:
            pass

    def get_property(self, prop):
        if prop == BufferBase.PROPERTY_READONLY:
            return self._readonly_document
        elif prop == BufferBase.PROPERTY_BOLD:
            return self._bold_on
        elif prop == BufferBase.PROPERTY_ITALIC:
            return self._italic_on
        elif prop == BufferBase.PROPERTY_UNDERLINE:
            return self._underline_on
        elif prop == BufferBase.PROPERTY_SELECTION:
            return self._selection_on
        else:
            return None

    def set_property(self, prop, value):
        assert isinstance(value, bool)
        if prop == BufferBase.PROPERTY_READONLY:
            self._readonly_document = value
        elif prop == BufferBase.PROPERTY_BOLD:
            self._bold_on = value
        elif prop == BufferBase.PROPERTY_ITALIC:
            self._italic_on = value
        elif prop == BufferBase.PROPERTY_UNDERLINE:
            self._underline_on = value
        elif prop == BufferBase.PROPERTY_SELECTION:
            self._selection_on = value
        else:
            raise ValueError('invalid property name')
    @property
    def is_selection_on(self):
        return self._selection_on
