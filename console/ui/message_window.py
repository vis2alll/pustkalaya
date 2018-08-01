from .window import Window, PromptWindow
from ..core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType
from ..core.keys import Keys
from ..core.keybinding import Registry


def load_message_prompt_bindings():
    registry = Registry(MessageWindow)
    handle = registry.add_binding

    def hide_window(event):
        event.current_window.hide()
        event.app.editor.pop_focus()

    @handle(Keys.Enter)
    @handle(Keys.Backspace)
    @handle(Keys.AltZ)
    @handle(Keys.ControlG)
    def _(event):
        window = event.app.editor.current_window

        if window.lock:
            window.lock.acquire()
            window.timer.cancel()
        try:
            on_ok = window.on_ok
            if on_ok is not None:
                on_ok(event)
            else:
                hide_window(event)
        finally:
            if window.lock:
                window.lock.release()

    return registry

class MessageWindow(PromptWindow):
    def __init__(self, message, *a, **ka):
        self.on_ok = ka.pop('on_ok', None)

        PromptWindow.__init__(self, message, *a, **ka)

