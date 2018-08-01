from ..enums import DEFAULT_WINDOW
from ..logger import logger
from .window import Window, PromptWindow
from .confirm_window import ConfirmationWindow
from .message_window import MessageWindow
from .textinput_window import TextInputWindow
from .selectfile_window import SelectFileWindow
from .menu_window import Menu
from ..core.event_type import EventType

import curses
import traceback

_logger = logger('editor')

class Editor(object):
    def __init__(self,
            edit_area_width,
            edit_area_height,
            prompt_row,
            prompt_height,
            prompt_width,
            windows = None,
            initial_focused_window = DEFAULT_WINDOW):

        self._edit_area_height = edit_area_width
        self._edit_area_width = edit_area_height
        self._prompt_row = prompt_row
        self._prompt_height = prompt_height
        self._prompt_width = prompt_width
        self.search_text = None
        self.replace_text = None
        self.back_search = False
        self._is_readonly = None # status of BufferBase.is_readonly of currently focused window

        if windows is None:
            windows = []

        assert all(isinstance(window, Window) for window in windows)

        self._windows = []
        self._focus_stack = []

        for w in windows:
            self.add_window(w)

        self.focus(initial_focused_window)
        self._force_refresh = False

    @property
    def current_window(self):
        return self.find_window(self._focus_stack[-1])

    def find_window(self, window_name):
        for window in self._windows:
            if window.name == window_name:
                return window
        return None

    def add_window(self, window):
        _logger.debug('adding %r to editor' % window)
        self._windows.append(window)
        self._focus_stack.append(window.name)
        self._force_refresh = True
        window.editor = self

        window.on(EventType.STATUS_BUSY, self.show_busy)
        window.on(EventType.STATUS_IDLE, self.show_idle)

    def remove_window(self, window):
        if isinstance(window, str):
            window = self.find_window(window)

        _logger.debug('Removing %r' % window)
        window.clear()
        window.refresh()
        self._windows.remove(window)
        self._force_refresh = True

    def focus(self, window_name):
        assert window_name is not None and len(window_name) > 0
        if window_name in self._focus_stack:
            self._focus_stack.remove(window_name)
        for w in self._windows:
            w.unfocus()
        self._focus_stack.append(window_name)
        self.current_window.show()
        self.current_window.focus()

    def pop_focus(self):

        # there should be minimum 1 window in focus stack
        if len(self._focus_stack) < 2:
            return

        top = self._focus_stack.pop()
        secondtop = self._focus_stack.pop()
        top_window = self.find_window(top)
        _logger.debug('popping %r' % top_window)
        if top_window and top_window.destroy_on_exit:
            self.remove_window(top_window)
        else:
            self._focus_stack.append(top)
        self._focus_stack.append(secondtop)
        self.current_window.show()
        self.current_window.focus()

    @property
    def is_dirty(self):
        return any(w.is_dirty for w in self._windows)

    def refresh(self):
        needs_update = False
        for window_name in self._focus_stack:
            window = self.find_window(window_name)
            if self._force_refresh or (window is not None and window.is_dirty):
                window.refresh()
                needs_update = True

        if needs_update:
            curses.doupdate()
        self._force_refresh = False

        is_readonly = self.current_window.buffer.is_readonly

        if self._is_readonly is not None and self._is_readonly == is_readonly:
            return

        self._is_readonly = is_readonly

    CONFIRM_WINDOW = 'CONFIRM_WINDOW'
    def confirm(self, prompt, on_yes_handler, on_no_handler, on_cancel_handler = None):
        window = ConfirmationWindow(prompt,
            name = Editor.CONFIRM_WINDOW,
            top = self._prompt_row,
            left = 0,
            rows = self._prompt_height,
            columns = self._prompt_width,
            wrap = False,
            visible = False,
            on_yes = on_yes_handler, on_no = on_no_handler, on_cancel = on_cancel_handler)

        self.add_window(window)

        self.focus(Editor.CONFIRM_WINDOW)

    BUSY_WINDOW = 'BUSY_WINDOW'
    def show_busy(self, message):
        window = self.find_window(Editor.BUSY_WINDOW)
        if window is None:
            window = MessageWindow(message,
                name = Editor.BUSY_WINDOW,
                top = self._prompt_row,
                left = 0,
                rows = self._prompt_height,
                columns = self._prompt_width,
                wrap = False,
                visible = False,
                on_ok = lambda e : None)

            self.add_window(window)
        else:
            window.prompt_text = message

        self.focus(Editor.BUSY_WINDOW)
        self._force_refresh = True
        self.refresh()

    def show_idle(self):
        window = self.find_window(Editor.BUSY_WINDOW)
        if window is not None:
            window.hide()
            if window == self.current_window:
                self.pop_focus()


    def input(self, prompt, name, on_ok_handler = None, on_cancel_handler = None, input_parser = None):
        window = self.find_window(name)
        if window is None:
            window = TextInputWindow(prompt,
                name = name,
                top = self._prompt_row,
                left = 0,
                rows = self._prompt_height,
                columns = self._prompt_width,
                wrap = False,
                visible = False,
                on_ok = on_ok_handler, on_cancel = on_cancel_handler, input_parser = input_parser)

            self.add_window(window)
        else:
            window.prompt_text = prompt

        self.focus(name)

    def create_menu(self, name, menus):
        window = self.find_window(name)
        if window is None:
            window = Menu(name = name,
                top = 0,
                left = 0,
                rows = self._edit_area_height,
                columns = self._edit_area_width,
                wrap = False,
                visible = False,
                menus = menus)

            self.add_window(window)

        self.focus(name)

    MESSAGE_WINDOW = 'MESSAGE_WINDOW'
    def message(self, message, hide_window = True, on_ok_handler = None):
        # if hide_window:
        #     self.current_window.hide()
        #     self.pop_focus()
        window = self.find_window(Editor.MESSAGE_WINDOW)
        if window is None:
            window = MessageWindow(message,
                name = Editor.MESSAGE_WINDOW,
                top = self._prompt_row,
                left = 0,
                rows = self._prompt_height,
                columns = self._prompt_width,
                wrap = False,
                visible = False,
                on_ok = on_ok_handler)

            self.add_window(window)
        else:
            window.prompt_text = message

        self.focus(Editor.MESSAGE_WINDOW)

    def error(self, message, hide_window = True, on_ok_handler = None):
        _logger.error('%r %r' % (message, traceback.format_exc()))
        self.message(message, hide_window, on_ok_handler)

    SELECT_FILE_WINDOW = 'SELECT_FILE_WINDOW'
    def select_file(self, current_path, prompt = None, on_file_selected_handler = None, on_cancel_handler = None):
        window = SelectFileWindow(current_path,
                name = Editor.SELECT_FILE_WINDOW,
                top = self._prompt_row,
                left = 0,
                rows = self._prompt_height,
                columns = self._prompt_width,
                wrap = False,
                visible = False,
                prompt = prompt,
                on_file_selected = on_file_selected_handler,
                on_cancel = on_cancel_handler)

        self.add_window(window)
        self.focus(Editor.SELECT_FILE_WINDOW)
