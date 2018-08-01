from .window import Window, PromptWindow
from ..core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType
from ..core.keys import Keys
from ..core.keybinding import Registry


def load_confirm_prompt_bindings():
    registry = Registry(ConfirmationWindow)
    handle = registry.add_binding

    def hide_prompt(event):
        event.current_window.hide()
        event.app.editor.pop_focus()

    @handle('Y')
    @handle('y')
    def _(event):
        on_yes = event.app.editor.current_window.on_yes
        on_yes_args = event.app.editor.current_window.on_yes_args
        hide_prompt(event)
        if on_yes is not None:
            if on_yes_args:
                on_yes(event, on_yes_args)
            else:
                on_yes(event)

    @handle('N')
    @handle('n')
    def _(event):
        on_no = event.app.editor.current_window.on_no
        on_no_args = event.app.editor.current_window.on_no_args
        hide_prompt(event)
        if on_no is not None:
            if on_no_args:
                on_no(event, on_no_args)
            else:
                on_no(event)

    @handle('C')
    @handle('c')
    @handle(Keys.AltZ)
    @handle(Keys.ControlG)
    def _(event):
        on_cancel = event.app.editor.current_window.on_cancel
        hide_prompt(event)
        if on_cancel is not None:
            on_cancel(event)

    return registry

class ConfirmationWindow(PromptWindow):
    def __init__(self, prompt, *a, **ka):
        self.on_yes = ka.pop('on_yes', None)
        self.on_cancel = ka.pop('on_cancel', None)
        self.on_no = ka.pop('on_no', None)
        self.on_yes_args = ka.pop('on_yes_args', None)
        self.on_no_args = ka.pop('on_no_args', None)

        PromptWindow.__init__(self, prompt, *a, **ka)
