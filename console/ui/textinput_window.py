from .window import Window, PromptWindow
from ..core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType
from ..core.keys import Keys
from ..core.keybinding import Registry
from ..logger import logger

import re

_logger = logger('text_input')

def load_textinput_bindings():
    registry = Registry(TextInputWindow)
    handle = registry.add_binding

    def hide_prompt(event, *a):
        event.current_window.hide()
        event.app.editor.pop_focus()

    @handle(Keys.AltZ)
    @handle(Keys.ControlG)
    def _(event):
        on_cancel = event.current_window.on_cancel
        if on_cancel is None:
            on_cancel = hide_prompt

        if hide_prompt != on_cancel:
            hide_prompt(event)
        on_cancel(event)

    @handle(Keys.Enter)
    def _(event):
        on_ok = event.current_window.on_ok

        if on_ok is None:
            on_ok = hide_prompt

        if event.current_window.buffer.text:
            result = event.current_window.input_parser.parse(event.current_window.buffer.text)
            if hide_prompt != on_ok:
                hide_prompt(event)
            on_ok(event, result)
        else:
            hide_prompt(event)

    @handle(Keys.ControlU)
    def _(event):
        event.current_window.buffer.text = ''

    return registry

class TextInputParser(object):
    def parse(self, text):
        return text.strip()

class RowColumnInputParser(TextInputParser):
    def __init__(self):
        self._re = re.compile('([1-9][0-9]*)\s*,?\s*([1-9][0-9]*)')
    def parse(self, text):
        text = text.strip()
        matches = self._re.finditer(text)
        groups = None
        for match in matches:
            groups = match.groups()
            break
        if not groups or len(groups) < 2:
            return None

        rows = (int)(match.group(1))
        columns = (int)(match.group(2))

        return (rows, columns)

class IntegerInputParser(TextInputParser):
    def __init__(self):
        self._re = re.compile('\s*([1-9][0-9]*)\s*')
    def parse(self, text):
        text = text.strip()
        matches = self._re.finditer(text)
        groups = None
        for match in matches:
            groups = match.groups()
            break
        if not groups or len(groups) < 1:
            return None

        val = (int)(match.group(1))

        return val

class TextInputWindow(PromptWindow):
    def __init__(self, prompt, *a, **ka):
        self.on_ok = ka.pop('on_ok', None)
        self.on_cancel = ka.pop('on_cancel', None)
        self.input_parser = ka.pop('input_parser', TextInputParser())

        if self.input_parser is None:
            self.input_parser = TextInputParser()

        PromptWindow.__init__(self, prompt, *a, **ka)
        self.buffer.is_readonly = False
