from .base import Filter
from ...logger import logger

_logger = logger('filter')

class HasFocus(Filter):
    def __init__(self, window_name):
        self._window_name = window_name

    def __call__(self, app):
        return app.editor.current_window.name == self._window_name

class HasBufferState(Filter):
    def __init__(self, buffer_state):
        self._buffer_state = buffer_state

    def __call__(self, app):
        return app.editor.current_window.buffer.state == self._buffer_state

class Readonly(Filter):
    def __init__(self, window_name):
        self._window_name = window_name

    def __call__(self, app):
        window = app.editor.find_window(self._window_name)
        return True if window is None else window.buffer.is_readonly

class WindowType(Filter):
    def __init__(self, window_type):
        self._window_type = window_type

    def __call__(self, app):
        return isinstance(app.editor.current_window, self._window_type)

class SupportsRichText(Filter):
    def __init__(self, window_name):
        self._window_name = window_name

    def __call__(self, app):
        window = app.editor.find_window(self._window_name)
        return False if window is None else window.buffer.supports_rich_text

class IsBlockType(Filter):
    def __init__(self, block_type):
        self._block_type = block_type

    def __call__(self, app):
        return app.editor.current_window.buffer.current_block_type == self._block_type

class HasPropertyOn(Filter):
    def __init__(self, prop):
        self._prop = prop

    def __call__(self, app):
        return app.editor.current_window.buffer.get_property(self._prop)
