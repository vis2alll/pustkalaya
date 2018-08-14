from console.core.keybinding import Registry, MergedRegistry
from console.core.keys import Keys
from console.enums import DEFAULT_WINDOW
from console.core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType, SupportsRichText, IsBlockType, HasPropertyOn
from console.core.filters.base import OrFilter, AndFilter, NotFilter
from console.ui.window import EditorWindow
from console.ui.menu_window import Menu, MenuItem
from console.core.buffer_base import BufferBase


def load_custom_binding():
    registry = Registry(EditorWindow)

    handle = registry.add_binding

    @handle(Keys.AltM)
    def _(e):
        # current_window = e.current_window
        # current_window = e.app.editor.current_window

        e.app.editor.message('message demo')

    @handle(Keys.AltE)
    def _(e):
        e.app.editor.error('error message demo')

    @handle(Keys.AltC)
    def _(e):
        def _on_yes(e):
            e.app.editor.message('you pressed yes')

        def _on_no(e):
            e.app.editor.message('you pressed no')

        e.app.editor.confirm('confirm?', on_yes_handler = _on_yes, on_no_handler = on_no)

    @handle(Keys.ControlH) # change highlighting bold/italic/underline
    def _(event):
        window_name = 'HIGHLIGHT'

        def _toggle_highlight(app, name):
            window = app.editor.find_window(DEFAULT_WINDOW)

            # if selection is not on enable/disable selected property
            window.buffer.toggle_property(name)
            state = window.buffer.get_property(name)
            if name == BufferBase.PROPERTY_BOLD:
                prop = 'bold'
            elif name == BufferBase.PROPERTY_ITALIC:
                prop = 'italic'
            elif name == BufferBase.PROPERTY_UNDERLINE:
                prop = 'underline'

            app.editor.message('%s %s' % (prop, 'enabled' if state else 'disabled'))

        event.app.editor.create_menu(window_name, [
            MenuItem('bold', 'b', lambda app: _toggle_highlight(app, BufferBase.PROPERTY_BOLD)),
            MenuItem('italic', 'i', lambda app: _toggle_highlight(app, BufferBase.PROPERTY_ITALIC)),
            MenuItem('underline', 'u', lambda app: _toggle_highlight(app, BufferBase.PROPERTY_UNDERLINE)),
                    ])

    return registry
