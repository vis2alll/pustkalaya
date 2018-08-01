from ..core.buffer_base import BufferBase
from .position import Position
from .size import Size
from ..enums import DEFAULT_WINDOW
from ..logger import logger
from ..config import KEY_INPUT_WAIT_TIMEOUT
from .highlighter import Highlighter
from ..core.event_type import EventType
from ..core.eventemitter import EventEmitter
from ..core.prompt_buffer import PromptBuffer

import curses, curses.panel
from textwrap import TextWrapper
import traceback
from threading import Timer, Lock

_logger = logger('window')

class Window(EventEmitter):
    def __init__(self,
            name = DEFAULT_WINDOW,
            top = 0,
            left = 0,
            rows = 25,
            columns = 80,
            wrap = True,
            visible = True,
            buf = None,
            highlighters = []):

        EventEmitter.__init__(self)

        assert top >= 0, 'top most row must be >= 0'
        assert left >= 0, 'left most column must be >= 0'
        assert rows > 0, 'window height must be positive value'
        assert columns > 0, 'window width must be positive value'
        assert buf is None or isinstance(buf, BufferBase)
        assert name is not None
        assert isinstance(wrap, bool)
        assert isinstance(highlighters, list) and all(isinstance(h, Highlighter) for h in highlighters)

        self._name = name
        self._text_changed = True       # set to true when buffer changes
        self._cursor_moved = visible       # set to true when cursor moves
        self._need_redraw = visible
        self._visible = visible
        self._has_focus = False
        self._textlines = []            # cahched lines these lines are created from buffer.text and converted to lines with word wrapping
        self._newlines = []    # set to True if a new line break is found (not because of word wrapping)
        self._toprow = 0                # from which line in self._textlines to display in current line
        self._leftcol = 0               # from which column in each line of self._textlines to display in current line
        self._num_prev_lines = 0        # number of lines painted in last refresh
        self._wrap = wrap
        self._highlighters = highlighters
        self.destroy_on_exit = False

        self._buffer = buf
        if self._buffer:
            self._buffer.name = name

            self._buffer.on(EventType.TEXT_CHANGED, self._on_text_changed)
            self._buffer.on(EventType.CURSOR_MOVED, self._on_cursor_moved)
            self._buffer.on(EventType.STATUS_BUSY, self._on_status_busy)
            self._buffer.on(EventType.STATUS_IDLE, self._on_status_idle)

        # initialize curses window
        self._curses_window = curses.newwin(rows, columns, top, left)
        self._curses_window.keypad(1)      # enable special keys, like, arrow, PageXX, etc.
        self._curses_window.timeout(KEY_INPUT_WAIT_TIMEOUT)
        self._panel = curses.panel.new_panel(self._curses_window)

    def _on_text_changed(self):
        self._text_changed = True
        self._need_redraw = True
    def _on_cursor_moved(self):
        self._cursor_moved = True
        self._has_focus = True

    def __repr__(self):
        return 'Window(%r)' % self.name

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, value):
        self._buffer = value

    @property
    def name(self):
        return self._name

    @property
    def is_dirty(self):
        return self._need_redraw or self._cursor_moved

    @property
    def curses_window(self):
        return self._curses_window

    @property
    def width(self):
        h,w = self._curses_window.getmaxyx()
        return w

    @property
    def height(self):
        h,w = self._curses_window.getmaxyx()
        return h

    @property
    def top(self):
        y,x = self._curses_window.getbegyx()
        return y

    @property
    def left(self):
        y,x = self._curses_window.getbegyx()
        return x

    @property
    def editable_width(self):
        return self.width

    @property
    def editable_height(self):
        return self.height

    @property
    def editable_top(self):
        return self.top

    @property
    def editable_left(self):
        return self.left

    @property
    def wrap(self):
        return self._wrap

    def show(self):
        if self.is_visible is False:
            self._need_redraw = True
        self._visible = True
        _logger.debug('%r is now visible' % self)

    def hide(self):
        _logger.debug('%r is currently %s' % (self, 'visible' if self.is_visible else 'hidden'))
        if self.is_visible is True:
            self._need_redraw = True
        self._visible = False
        _logger.debug('%r is now hidden' % self)

    def focus(self):
        if not self._has_focus:
            self._need_redraw = True
        self._has_focus = True
        self.buffer.focus()
    def unfocus(self):
        if self._has_focus:
            self._need_redraw = True
        self._has_focus = False

    @property
    def is_visible(self):
        return self._visible

    @property
    def lines(self):
        """
        split buffer text to lines handling word wrapping
        """
        if self.wrap:
            if self._text_changed:
                # -1 is to allow cursor to be placed at the end of the column
                textwrapper = TextWrapper(width = self.editable_width - 1, drop_whitespace = False)
                text = self.buffer.text

                # we need to first split text into paragraphs so that it does not cuase strange output
                # limitation of TextWrapper
                paragraphs = text.splitlines()
                self._textlines = []
                self._newlines = []


                if len(text) > 0 and text[-1] == '\n':
                    paragraphs.append('')

                if len(paragraphs) == 1 and text[-1] != '\n': # no new lines in between
                    textlines = textwrapper.wrap(paragraphs[0])
                    for line in textlines:
                        self._newlines.append(False)
                    self._textlines.extend(textlines)
                else:
                    for p in paragraphs:
                        textlines = textwrapper.wrap(p)
                        if len(textlines) > 0:
                            i = 0
                            while i < len(textlines) - 1:
                                self._newlines.append(False)
                                i += 1
                            self._newlines.append(True)
                            self._textlines.extend(textlines)
                        else:
                            self._newlines.append(True)
                            self._textlines.append('')
        else:
            if len(self.buffer.text) > 0:
                self._textlines = [self.buffer.text]
                self._newlines = [False]
            else:
                self._textlines = []
                self._newlines = []

        return self._textlines
    def _on_status_busy(self, *a):
        self.emit(EventType.STATUS_BUSY, *a)

    def _on_status_idle(self):
        self.emit(EventType.STATUS_IDLE)

    @property
    def newlines(self):
        return self._newlines

    def row_column_from_cursor(self, pos = None):
        # find cursor row and column
        row = 0
        cursor = 0
        newline_count = 0
        lines = self.lines

        if pos is None:
            pos = self.buffer.cursor

        linecount = len(lines)

        while (row < linecount and
                ((row < linecount - 1 and
                    cursor + len(lines[row]) + (1 if self._newlines[row] else 0) <= pos) or
                  (row == linecount - 1 and
                    cursor + len(lines[row]) + (1 if self._newlines[row] else 0) < pos))):
            cursor += len(lines[row]) + (1 if self._newlines[row] else 0)
            row += 1

        pos -= cursor

        col = pos
        # if pos == len (lines[row]):
        #     col += (1 if self._newlines[row] else 0)

        # row = 0
        # cursor = 0
        # while (row < linecount and
        #         (row < linecount - 1 and
        #             cursor + len(lines[row]) <= pos) or # not last line
        #         (row == linecount - 1 and
        #             cursor + len(lines[row]) < pos) # last line
        #         ):
        #     cursor += len(lines[row])
        #     row += 1

        # col = pos - cursor

        return row, col

    def cursor_from_row_column(self, row, col):
        # find cursor row and column
        cursor = 0
        lines = self.lines
        start = 0

        if len(lines) == 0:
            return 0
        while start < row:
            cursor += len(lines[start]) + (1 if self._newlines[start] else 0)
            start += 1

        cursor += (col if col <= len(lines[start]) else
                (len(lines[start]) + (0)))
        return cursor

    def refresh(self):
        try:
            if not self.is_visible:
                if self._need_redraw:
                    rows = self.height
                    while rows > 0:
                        rows -= 1
                        self._curses_window.move(rows, 0)
                        self._curses_window.clrtoeol()
            else:
                textlines = self.lines
                # _logger.debug('textlines %r' % textlines)
                # current row and column of the cursor
                row, col = self.row_column_from_cursor()

                if row < self._toprow:
                    self._need_redraw = True
                    self._toprow = row
                elif row >= self._toprow + self.editable_height:
                    self._need_redraw = True
                    self._toprow = row - self.editable_height + 1

                if col < self._leftcol:
                    self._need_redraw = True
                    self._leftcol = col
                elif col >= self._leftcol + self.editable_width:
                    self._need_redraw = True
                    self._leftcol = col - self.editable_width + 1

                if self._text_changed:
                    self._need_redraw = True

                if self._need_redraw:
                    linecount = 0
                    row = self._toprow

                    if len(textlines) == 0: # clear the first line when there is no text to be displayed, rest will be handled below
                        self._curses_window.clrtoeol()

                    while row < len(textlines) and linecount < self.editable_height:
                        cursor_row = linecount + self.editable_top - self.top
                        cursor_col = self.editable_left - self.left
                        line = textlines[row]

                        if len(line) > 0:
                            line = line[self._leftcol:self._leftcol + self.editable_width]

                        # _logger.debug('painting %r at row,col %r %r with line len %r' %
                        #         (self, cursor_row, cursor_col, len(line)))

                        self._curses_window.move(cursor_row, cursor_col)
                        self._curses_window.clrtoeol()
                        self._curses_window.addstr(cursor_row, cursor_col, line.encode("utf-8"))
                        row += 1
                        linecount += 1

                    for highlighter in self._highlighters:
                        highlighter.activate(self)


                    while linecount < self._num_prev_lines:
                        cursor_row = linecount + self.editable_top - self.top
                        cursor_col = self.editable_left - self.left
                        self._curses_window.move(cursor_row, cursor_col)
                        self._curses_window.clrtoeol()
                        linecount += 1

                    self._num_prev_lines = min(len(textlines), self.editable_height)

                # set cursor position
                if self._has_focus:
                    row, col = self.row_column_from_cursor()

                    # _logger.debug('%r row, col: %d,%d from row_column_from_cursor' % (self, row, col))

                    # _logger.debug('%r moving cursor to row, col: %d,%d' %
                    #         (self, row - self._toprow + self.editable_top,
                    #         col - self._leftcol + self.editable_left))

                    self._curses_window.move(row - self._toprow + self.editable_top - self.top,
                            col - self._leftcol + self.editable_left - self.left)

            if self._cursor_moved or self._need_redraw:
                self._curses_window.noutrefresh()
        except:
            _logger.error('some error occurred while displaying %r' % traceback.format_exc())
            pass

        self._text_changed = False
        self._cursor_moved = False
        self._need_redraw = False

    def highlight(self, attr, row, col, length = 1):
        if row < self._toprow or row >= self._toprow + self.editable_height:
            return
        self._curses_window.chgat(row - self._toprow, col - self._leftcol, length, attr)

    def clear(self):
        self._curses_window.clear()
        self._need_redraw = True

    @property
    def toprow(self):
        return self._toprow

    @toprow.setter
    def toprow(self, value):
        if value < len(self.lines):
            self._toprow = value

    def force_refresh(self):
        self._need_redraw = True

class EditorWindow(Window):
    pass

class PromptWindow(Window):
    def __init__(self, prompt, *a, **ka):
        _timeout = ka.pop('timeout', None)
        Window.__init__(self,
                buf = PromptBuffer(),
                *a,
                **ka)
        self._prompt = prompt
        self.destroy_on_exit = True
        self.buffer.is_readonly = True
        self._reset = True

        self.lock = None
        self.timer = None

        def _exit(self):
            self.lock.acquire()
            self.timer.cancel()
            try:
                self.hide()
                self.editor.pop_focus()
            finally:
                self.lock.release()

        if _timeout is not None:
            self.lock = Lock()
            self.timer = Timer(_timeout, _exit, args = [self])

    @property
    def prompt_text(self):
        if self._prompt:
            return '%s ' % self._prompt

        return ''

    @prompt_text.setter
    def prompt_text(self, value):
        _logger.debug('%r setting prompt text to %r' % (self, value))
        self._prompt = value
        self._need_redraw = True
        self._reset = True

    @property
    def editable_width(self):
        return self.width - len(self.prompt_text)

    @property
    def editable_left(self):
        return self.left + len(self.prompt_text)

    def refresh(self):
        # _logger.debug('%r is currentlty %s and needs redraw: %s' % (self,
        #     'visble' if self.is_visible else 'hidden',
        #     self._need_redraw))

        if self.is_visible and self._need_redraw:
            self._curses_window.move(0, 0)
            self._curses_window.clear()
            self._curses_window.addstr(0, 0, self.prompt_text)
            self._need_redraw = False
        Window.refresh(self)
        if self._reset:
            self._reset = False

    def show(self):
        Window.show(self)
        if not self.lock:
            return
        self.lock.acquire()
        try:
            self.timer.start()
        finally:
            self.lock.release()

    def hide(self):
        Window.hide(self)
        if not self.lock:
            return
        self.lock.acquire()
        try:
            self.cancel()
        finally:
            self.lock.release()
