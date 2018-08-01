from .core.filters.basic import HasFocus, HasBufferState, Readonly
from .core.filters.base import OrFilter, AndFilter
from .core.keybinding import Registry
from .core.keys import Keys
from .enums import DEFAULT_WINDOW
from .core.bufferstate import BufferState
from .core.findnreplace import FindNReplace
from .logger import logger
from .core.buffer_base import BufferBase
from .ui.window import EditorWindow

SEARCH_WINDOW = 'SEARCH_WINDOW'
REPLACE_WINDOW = 'REPLACE_WINDOW'

_logger = logger('search')

def load_search_n_replace_bindings():
    registry = Registry(EditorWindow)
    handle = registry.add_binding

    editing_window_has_focus = HasFocus(DEFAULT_WINDOW)
    search_window_has_focus = HasFocus(SEARCH_WINDOW)
    replace_window_has_focus = HasFocus(REPLACE_WINDOW)
    editing = HasBufferState(BufferState.EDITING)

    can_search = AndFilter(editing_window_has_focus, editing)

    def _handle_search_result(event, result):
        if result == FindNReplace.NO_MATCH_FOUND or result == FindNReplace.NO_MORE_MATCHES:
            event.app.editor.message(result)
        elif result == FindNReplace.SEARCH_FROM_TOP:
            event.app.editor.confirm(('search from top?' if
                not event.app.editor.back_search else
                'search from bottom?'), _search_from_top, None)

    def _search_from_top(event):
         result = event.current_window.buffer.next_match(event.app.editor.search_text,
                 back_search = event.app.editor.back_search, from_top = True)
         _handle_search_result(event, result)


    @handle(Keys.Enter, filter = search_window_has_focus)
    def _on_search_ok(event, search_text):
        editor = event.app.editor
        editor.search_text = search_text

        if editor.replace:
            get_replace_input(event)
        else:
            editor.focus(DEFAULT_WINDOW)
            try:
                result = editor.current_window.buffer.next_match(search_text,
                        back_search = event.app.editor.back_search)
                _handle_search_result(event, result)
            except:
                    event.app.editor.error('error while searching')


    def _on_reaplce_ok(event, replace_text):
        editor = event.app.editor
        editor.replace_text = replace_text

        editor.focus(DEFAULT_WINDOW)
        try:
            result = editor.current_window.buffer.next_match(editor.search_text,
                    back_search = event.app.editor.back_search)
            _handle_search_result(event, result)
        except:
            event.app.editor.error('error while searching')

    def get_search_input(event):
        event.app.editor.replace = False
        if not event.app.editor.back_search:
            event.app.editor.input('search:',
                    SEARCH_WINDOW,
                    on_ok_handler = _on_search_ok)
        else:
            event.app.editor.input('back-search:',
                    SEARCH_WINDOW,
                    on_ok_handler = _on_search_ok)

    def get_replace_input(event):
        event.app.editor.input('replace with:',
                REPLACE_WINDOW,
                on_ok_handler = _on_reaplce_ok)

    @handle(Keys.ControlF, filter = OrFilter(can_search, replace_window_has_focus))
    def _(event):
        event.current_window.buffer.reset_search()
        if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
            event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
        get_search_input(event)

    @handle(Keys.ControlR, filter = OrFilter(can_search, search_window_has_focus))
    def _(event):
        window = event.app.editor.find_window(DEFAULT_WINDOW)
        if window.buffer.is_readonly:
            event.app.editor.message('document is read only')
            return
        event.current_window.buffer.reset_search()
        if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
            event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
        get_search_input(event)
        event.app.editor.replace = True

    @handle(Keys.ControlT, filter = OrFilter(replace_window_has_focus, search_window_has_focus))
    def _(event):
        event.app.editor.back_search = not event.app.editor.back_search
        get_search_input(event)


    @handle(Keys.ControlC, filter = OrFilter(search_window_has_focus, replace_window_has_focus))
    def _(event):
        event.app.editor.search_text = None
        event.app.editor.replace_text = None
        event.app.editor.replace = False

        search_window = event.app.editor.find_window(SEARCH_WINDOW)
        replace_window = event.app.editor.find_window(REPLACE_WINDOW)

        if search_window:
            search_window.hide()
        if replace_window:
            replace_window.hide()

        event.app.editor.focus(DEFAULT_WINDOW)

    @handle(Keys.ControlK, filter = editing_window_has_focus)
    def _(event):
        try:
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
            result = event.app.editor.current_window.buffer.next_match(event.app.editor.search_text,
                    back_search = event.app.editor.back_search)
            _handle_search_result(event, result)

        except:
            event.app.editor.error('error while searching')

    @handle(Keys.AltK, filter = editing_window_has_focus)
    def _(event):
        try:
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
            result = event.app.editor.current_window.buffer.next_match(event.app.editor.search_text,
                    back_search = not event.app.editor.back_search)
            _handle_search_result(event, result)

        except:
            event.app.editor.error('error while searching')

    @handle(Keys.ControlL, filter = editing_window_has_focus)
    def _(event):
        if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
            event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
        try:
            editor = event.app.editor
            result = editor.current_window.buffer.replace(editor.search_text, editor.replace_text,
                    back_search = event.app.editor.back_search)
            _handle_search_result(event, result)
        except:
            event.app.editor.error('error while replacing')

    @handle(Keys.ControlA, filter = editing_window_has_focus)
    def _(event):
        editor = event.app.editor
        editor_window = editor.current_window
        if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
            event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)
        if editor.search_text and editor.replace_text:
            try:
                editor_window.buffer.replace_all(editor.search_text,
                        editor.replace_text,
                        back_search = event.app.editor.back_search)
                event.app.editor.message('all occurances replaced')
            except:
                event.app.editor.error('error while replacing')

    return registry
