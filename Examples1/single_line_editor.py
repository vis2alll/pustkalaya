import sys
sys.path.append('C:\Users\DELL\Desktop\RBD_dir\Editor_rbc\UIFramework')

import console

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

    @handle(Keys.AltI)
    def _(e):
		def _on_ok(evt, text):
			evt.app.editor.message('hello ' + text)
		def _on_cancel(evt):
			evt.app.editor.message('cancelled')
		e.app.editor.input('username:', 'username', on_ok_handler = _on_ok, on_cancel_handler = _on_cancel)

    @handle(Keys.AltM)
    def _(e):
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

        e.app.editor.confirm('confirm?', on_yes_handler = _on_yes, on_no_handler = _on_no)

    @handle(Keys.AltW)
    def _(e):
		buffer = e.app.editor.find_window(DEFAULT_WINDOW).buffer
		curr_buffer = e.current_window.buffer

		e.app.editor.message(buffer.text)


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


def main(stdscr, args):
    top, left = stdscr.getbegyx() # top left coordinate of the screen
    rows, cols = stdscr.getmaxyx() # size of screen

    console.init(stdscr)

    from console.logger import logger

    _logger = logger('main')

    try:
        from os import path
        import traceback
        from console.application import Application
        from console.ui.editor import Editor
        from console.ui.window import EditorWindow, PromptWindow
        from console.enums import DEFAULT_WINDOW
        from console.config import PROMPT_HEIGHT
        from console.core.prompt_buffer import PromptBuffer

        _logger.debug('terminal size %dx%d' % (rows, cols))

        edit_buffer = PromptBuffer()
        edit_buffer.is_readonly = False

        editwindow = EditorWindow(name = DEFAULT_WINDOW,
                top = top,
                left = left,
                rows = rows - PROMPT_HEIGHT,
                columns = cols,
                buf = edit_buffer,
                wrap = False)

        editor = Editor(
                rows - PROMPT_HEIGHT, 	# editable area height
                cols,			# editable area width
                rows - PROMPT_HEIGHT,	# prompt row
                PROMPT_HEIGHT,		# height of prompt window(1)
                cols,
                windows = [editwindow],
                initial_focused_window = DEFAULT_WINDOW)

        registry = MergedRegistry([
            console.default_bindings(),
            load_custom_binding()
            ])

        app = Application(editor, registry = registry)

        app.run()
    except:
        _logger.error('application exited with exception: %r' % traceback.format_exc())
        raise
    finally:
        pass


console.run(main, sys.argv)
