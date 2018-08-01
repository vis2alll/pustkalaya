from .core.keybinding import Registry, MergedRegistry
from .core.keys import Keys
from .logger import logger
from .enums import DEFAULT_WINDOW
from .core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType, SupportsRichText, IsBlockType, HasPropertyOn
from .core.filters.base import OrFilter, AndFilter, NotFilter
from .core.io.bufferio import Direction
from .core.bufferstate import BufferState
from .ui.menu_window import Menu, MenuItem
from .ui.window import EditorWindow
from .core.buffer_base import BufferBase
from os import path

_logger = logger('bindings')

def load_default_key_bindings():
    registry = Registry()

    handle = registry.add_binding

    # add default handler for keys

    @handle(Keys.Escape)
    @handle(Keys.ControlA)
    @handle(Keys.ControlB)
    @handle(Keys.ControlC)
    @handle(Keys.ControlD)
    @handle(Keys.ControlE)
    @handle(Keys.ControlF)
    @handle(Keys.ControlG)
    @handle(Keys.ControlH)
    @handle(Keys.ControlI)
    @handle(Keys.ControlJ)
    @handle(Keys.ControlK)
    @handle(Keys.ControlL)
    @handle(Keys.ControlM)
    @handle(Keys.ControlN)
    @handle(Keys.ControlO)
    @handle(Keys.ControlP)
    @handle(Keys.ControlQ)
    @handle(Keys.ControlR)
    @handle(Keys.ControlS)
    @handle(Keys.ControlT)
    @handle(Keys.ControlU)
    @handle(Keys.ControlV)
    @handle(Keys.ControlW)
    @handle(Keys.ControlX)
    @handle(Keys.ControlY)
    @handle(Keys.ControlZ)
    @handle(Keys.Alt0)
    @handle(Keys.Alt1)
    @handle(Keys.Alt2)
    @handle(Keys.Alt3)
    @handle(Keys.Alt4)
    @handle(Keys.Alt5)
    @handle(Keys.Alt6)
    @handle(Keys.Alt7)
    @handle(Keys.Alt8)
    @handle(Keys.Alt9)
    @handle(Keys.AltA)
    @handle(Keys.AltB)
    @handle(Keys.AltC)
    @handle(Keys.AltD)
    @handle(Keys.AltE)
    @handle(Keys.AltF)
    @handle(Keys.AltG)
    @handle(Keys.AltH)
    @handle(Keys.AltI)
    @handle(Keys.AltJ)
    @handle(Keys.AltK)
    @handle(Keys.AltL)
    @handle(Keys.AltM)
    @handle(Keys.AltN)
    @handle(Keys.AltO)
    @handle(Keys.AltP)
    @handle(Keys.AltQ)
    @handle(Keys.AltR)
    @handle(Keys.AltS)
    @handle(Keys.AltT)
    @handle(Keys.AltU)
    @handle(Keys.AltV)
    @handle(Keys.AltW)
    @handle(Keys.AltX)
    @handle(Keys.AltY)
    @handle(Keys.AltZ)
    @handle(Keys.AltEnter)
    @handle(Keys.AltF4)
    @handle(Keys.ControlSquareClose)
    @handle(Keys.ControlUnderscore)
    @handle(Keys.Up)
    @handle(Keys.Down)
    @handle(Keys.Right)
    @handle(Keys.Left)
    @handle(Keys.Home)
    @handle(Keys.End)
    @handle(Keys.Delete)
    @handle(Keys.ShiftDelete)
    @handle(Keys.PageUp)
    @handle(Keys.PageDown)
    @handle(Keys.BackTab)
    @handle(Keys.Insert)
    @handle(Keys.Backspace)
    @handle(Keys.Tab)
    @handle(Keys.Enter)
    @handle(Keys.F1)
    @handle(Keys.F2)
    @handle(Keys.F3)
    @handle(Keys.F4)
    @handle(Keys.F5)
    @handle(Keys.F6)
    @handle(Keys.F7)
    @handle(Keys.F8)
    @handle(Keys.F9)
    @handle(Keys.F10)
    @handle(Keys.F11)
    @handle(Keys.F12)
    @handle(Keys.F13)
    @handle(Keys.F14)
    @handle(Keys.F15)
    @handle(Keys.F16)
    @handle(Keys.F17)
    @handle(Keys.F18)
    @handle(Keys.F19)
    @handle(Keys.F20)
    @handle(Keys.F21)
    @handle(Keys.F22)
    @handle(Keys.F23)
    @handle(Keys.F24)
    def _(event):
        _logger.warn('unknown key: %r', event.key)

    @handle(Keys.Any)
    def _(event):
        try:
            if (event.code > 0x0 and event.code <= 0x80):
                event.current_window.buffer.insert_text(event.code)
        except Exception as e:
            event.app.editor.error('error while editing %r' % e)

    return registry

selection_on = HasPropertyOn(BufferBase.PROPERTY_SELECTION)
def load_basic_key_bindings():
    registry = Registry(EditorWindow)
    handle = registry.add_binding

    editing_window_has_focus = HasFocus(DEFAULT_WINDOW)
    buffer_is_readonly = Readonly(DEFAULT_WINDOW)
    editing = AndFilter(HasBufferState(BufferState.EDITING), editing_window_has_focus)

    @handle(Keys.AltX)
    def _(event):
        event.app.stop()

    @handle(Keys.Enter)
    def _(event):
        try:
            event.current_window.buffer.enter()
        except Exception as e:
            event.app.editor.error('unknown error %r' % e)

    @handle(Keys.Up)
    def _(event):
        try:
            row, col = event.current_window.row_column_from_cursor()
            if row > 0:
                row -= 1
                if row < event.current_window.toprow:
                    event.current_window.toprow -= event.current_window.editable_height
                    event.current_window.force_refresh()
                event.current_window.buffer.cursor = event.current_window.cursor_from_row_column(row, col)
            else:
                if event.current_window.buffer.cursor_up():
                    row = len(event.current_window.lines) - 1
                    event.current_window.buffer.cursor = event.current_window.cursor_from_row_column(row, 0)
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except Exception as e:
            event.app.editor.error('unable to navigate %r' % e)

    @handle(Keys.Down)
    def _(event):
        try:
            row, col = event.current_window.row_column_from_cursor()
            if row < len(event.current_window.lines) - 1:
                row += 1
                if row >= event.current_window.toprow + event.current_window.editable_height:
                    event.current_window.toprow += event.current_window.editable_height
                    event.current_window.force_refresh()
                event.current_window.buffer.cursor = event.current_window.cursor_from_row_column(row, col)
            else:
                event.current_window.buffer.cursor_down()
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except Exception as e:
            event.app.editor.error('unable to navigate %r' % e)

    # navigation commands

    @handle(Keys.ControlB, filter = editing)
    def _(event):
        try:
            event.current_window.buffer.top()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.ControlE, filter = editing)
    def _(event):
        try:
            event.current_window.buffer.bottom()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.PageDown, filter = editing_window_has_focus)
    def _(event):
        try:
            window = event.current_window
            if not (window.toprow + window.editable_height < len(window.lines)):
                if not event.current_window.buffer.next(None):
                    pass
                return

            newrow = window.toprow + window.editable_height
            window.buffer.cursor = window.cursor_from_row_column(newrow, 0)
            window.toprow = newrow
            window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.PageUp, filter = editing_window_has_focus)
    def _(event):
        try:
            window = event.current_window
            if window.toprow == 0:
                if not event.current_window.buffer.previous(None):
                    pass #event.app.editor.timedmessage('bottom of the document')
                else:
                    window.buffer.cursor_end()
                return
            newrow = window.toprow - window.editable_height
            window.buffer.cursor = window.cursor_from_row_column(newrow, 0)
            window.toprow = newrow
            window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.F9, filter = editing_window_has_focus)
    def _(event):
        event.current_window.buffer.toggle_property(BufferBase.PROPERTY_SELECTION)

    @handle(Keys.ControlC, filter = selection_on)
    def _(event):
        try:
            event.current_window.buffer.clipboard_copy()
            event.app.editor.message('text copied')
        except:
            event.app.editor.error('error in copying')
    @handle(Keys.ControlX, filter = selection_on)
    def _(event):
        try:
            if event.current_window.buffer.is_readonly:
                event.app.editor.message('document is read only')
            else:
                event.current_window.buffer.clipboard_cut()
                event.app.editor.message('text cut')
        except:
            event.app.editor.error('error in cut')
    @handle(Keys.ControlV)
    def _(event):
        try:
            if event.current_window.buffer.is_readonly:
                event.app.editor.message('document is read only')
            else:
                event.current_window.buffer.clipboard_paste()
        except:
            event.app.editor.error('error in paste')

    return MergedRegistry([registry, line_editing_key_bindings()])


def line_editing_key_bindings():
    registry = Registry()
    handle = registry.add_binding

    @handle(Keys.Backspace)
    def _(event):
        try:
            event.current_window.buffer.remove(-1)
        except:
            event.app.editor.error('unknown error')

    @handle(Keys.Delete)
    def _(event):
        try:
            event.current_window.buffer.remove(1)
        except:
            event.app.editor.error('unknown error')
    @handle(Keys.Left)
    def _(event):
        try:
            event.current_window.buffer.cursor_left()
            row, col = event.current_window.row_column_from_cursor()
            if row < event.current_window.toprow:
                event.current_window.toprow -= event.current_window.editable_height
                event.current_window.force_refresh()
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.Right)
    def _(event):
        try:
            event.current_window.buffer.cursor_right()
            row, col = event.current_window.row_column_from_cursor()
            if row >= event.current_window.toprow + event.current_window.editable_height:
                event.current_window.toprow += event.current_window.editable_height
                event.current_window.force_refresh()
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')
    @handle(Keys.Home)
    def _(event):
        try:
            row, col = event.current_window.row_column_from_cursor()
            event.current_window.buffer.cursor = event.current_window.cursor_from_row_column(row, 0)
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')

    @handle(Keys.End)
    def _(event):
        try:
            row, col = event.current_window.row_column_from_cursor()
            lines = event.current_window.lines
            newlines = event.current_window.newlines
            if row == len(lines) - 1:
                lastcol = len(lines[row])
            else:
                lastcol = len(lines[row]) - 1

            lastcol += (1 if newlines[row] else 0)
            event.current_window.buffer.cursor = event.current_window.cursor_from_row_column(row, lastcol)
            if event.current_window.buffer.get_property(BufferBase.PROPERTY_SELECTION):
                event.current_window.force_refresh()
        except:
            event.app.editor.error('unable to navigate')

    return registry
