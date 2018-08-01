 #  ------------------------------------------------------------------------------
 #  Copyright (c) Kritikal Solutions Pvt. Ltd.
 #  All rights Reserved
 #  ------------------------------------------------------------------------------
 #  Title               : selectfile_window
 #  Project             : WT_ARBD
 #  Author              : Vikash Kesarwani (vikash.kesarwani@kritikalsolutions.com)
 #  Company             : Kritikal Solutions Pvt. Ltd.
 #  Platform            : Linux
 #  Created             : Thursday Dec 28, 2017 18:40:14 IST
 #  ------------------------------------------------------------------------------
 #  Description         : window to browse and select a file path for save as
 #  ------------------------------------------------------------------------------

from .window import Window, PromptWindow
from ..core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType
from ..core.keys import Keys
from ..core.keybinding import Registry
from ..logger import logger
from ..enums import DEFAULT_WINDOW
from os import path

_logger = logger('select file')

def load_select_file_prompt_bindings():
    registry = Registry(SelectFileWindow)
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
        on_file_selected = event.current_window.on_file_selected

        if on_file_selected is None:
            on_file_selected = hide_prompt

        text = event.current_window.buffer.text.strip()
        if text:
            current_path = event.current_window.current_path
            new_path = text + event.current_window.ext
            directory = path.dirname(current_path)
            if hide_prompt != on_file_selected:
                hide_prompt(event)

            on_file_selected(event, current_path, path.join(directory, new_path))
        else:
            hide_prompt(event)

    @handle(Keys.ControlU)
    def _(event):
        event.current_window.buffer.text = ''

    return registry

class SelectFileWindow(PromptWindow):
    def __init__(self, current_path, *a, **ka):
        self.current_path =  '' if current_path is None else current_path
        self.on_file_selected = ka.pop('on_file_selected', None)
        self.on_cancel = ka.pop('on_cancel', None)
        _prompt = ka.pop('prompt', 'file name:')

        if not _prompt:
            _prompt = 'file name:'

        PromptWindow.__init__(self, _prompt, *a, **ka)
        name, ext = path.splitext(path.basename(self.current_path))
        self.buffer.text = name
        self.ext = ext
        self.buffer.is_readonly = False
