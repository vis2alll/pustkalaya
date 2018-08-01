from __future__ import unicode_literals
from .eventemitter import EventEmitter

from ..logger import logger
from .range import Range
from .event_type import EventType
from .bufferstate import BufferState

from re import finditer, IGNORECASE, escape as escape_regex_str
from abc import ABCMeta, abstractmethod
from six import with_metaclass
import traceback

class BufferBase(with_metaclass(ABCMeta, EventEmitter)):
    _logger = logger('buffer')

    PROPERTY_READONLY = 'PROPERTY_READONLY'
    PROPERTY_BOLD = 'PROPERTY_BOLD'
    PROPERTY_ITALIC = 'PROPERTY_ITALIC'
    PROPERTY_UNDERLINE = 'PROPERTY_UNDERLINE'
    PROPERTY_SELECTION = 'PROPERTY_SELECTION'

    def __init__(self, name = ''):
        EventEmitter.__init__(self)

        self._cursor = 0
        self.name = name
        self._readonly_document = True

        # formatting related
        self._bold_on = False
        self._bold_forced_on = False
        self._italic_on = False
        self._italic_forced_on = False
        self._underline_on = False
        self._underline_forced_on = False
        self._selection_on = False

        self.emit(EventType.TEXT_CHANGED)

    def __repr__(self):
        return 'BufferBase[%s]' % self.name

    def focus(self):
        """ do nothing """
        pass

    @property
    def text(self):
        """
        return text which to be displayed on the window
        if you need to display an array of lines then concatenate them with new line character ('\n')
        """
        raise NotImplementedError

    @text.setter
    def text(self, value):
        """
        set update text of the buffer
        after updating the text you must emit an TEXT_CHANGED event to notify the window so that
        it can be refreshed
                self.emit(EventType.TEXT_CHANGED)
        \param value new text
        \paramtype value string
        """
        raise NotImplementedError

    @property
    def cursor(self):
        """
        returns current cursor position in the text returned by self.text
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        """
        updated cursor position you must emit an CURSOR_MOVED event so that it can be refreshed
                self.emit(EventType.CURSOR_MOVED)
        \param value cursor position in text returned by self.text
        \paramtype value int
        """
        raise NotImplementedError

    @property
    def is_readonly(self):
        """
        return whether the buffer is readonly or editable
        """
        return self._readonly_document


    @is_readonly.setter
    def is_readonly(self, value):
        self._readonly_document = value

    @property
    def state(self):
        return BufferState.EDITING

    @property
    def selection_range(self):
        """
        return current selection range (instance of Range), which needs to be highligted
        """
        return None

    @property
    def format_ranges (self):
        """
        return an array of InlineFormatRange
        """
        return []

    def insert_text(self, ch):
        """
        insert 'ch' into current buffer at current cursor position
        \param ch character to be inserted (ch contains ascii value of the character to be inserted)
        \paramtype ch int
        """
        if self.is_readonly:
            BufferBase._logger.debug('buffer is readonly')
            return
        pass

    def remove(self, count = -1):
        """
        remove characters from the buffer from current cursor position
        \param count number of characters to remove, positive number denotes remove from the right
               of the cursor, negative denotes, remove from the left
        \paramtype count int
        """
        if self.is_readonly:
            BufferBase._logger.debug('buffer is readonly')
            return
        pass

    @abstractmethod
    def enter(self):
        """
        called when ENTER key is pressed
        """
        raise NotImplementedError

    @abstractmethod
    def cursor_up(self, rows = 1):
        """
        called when UP ARROW key is pressed
        """
        raise NotImplementedError

    @abstractmethod
    def cursor_down(self, rows = 1):
        """
        called when DOWN ARROW key is pressed
        """
        raise NotImplementedError

    @abstractmethod
    def cursor_left(self, cols = 1):
        """
        called when LEFT ARROW key is pressed
        """
        raise NotImplementedError

    @abstractmethod
    def cursor_right(self, cols = 1):
        """
        called when RIGHT ARROW key is pressed
        """
        raise NotImplementedError

    def cursor_beg(self):
        """
        called when HOME key is pressed
        """
        pass

    def cursor_end(self):
        """
        called when END key is pressed
        """
        pass

    @abstractmethod
    def top(self):
        """
        called when go to top command is executed
        """
        raise NotImplementedError

    @abstractmethod
    def bottom(self):
        """
        called when go to bottom command is executed
        """
        raise NotImplementedError

    def previous(self, blocktype):
        """
        needed in block wise loading
        """
        return None

    def next(self, blocktype):
        """
        needed in block wise loading
        """
        return None

    def delete(self):
        """
        called when DELETE key is pressed
        """
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
