from .window import Window, PromptWindow
from ..core.filters.basic import HasFocus, HasBufferState, Readonly, WindowType
from ..core.keys import Keys
from ..core.keybinding import Registry
from ..logger import logger
from ..enums import DEFAULT_WINDOW

_logger = logger('menu')


def load_menu_bindings():
    registry = Registry(Menu)
    handle = registry.add_binding

    def hide_window(event):
        event.current_window.hide()
        event.app.editor.pop_focus()

    @handle(Keys.Up)
    @handle(Keys.PageUp)
    def _(event):
        event.current_window.prev_menu()

    @handle(Keys.Down)
    @handle(Keys.PageDown)
    def _(event):
        event.current_window.next_menu()

    @handle(' ')
    def _(event):
        event.current_window.next_menu(cycle = True)

    @handle(Keys.Any)
    def _(event):
        event.current_window.enter_menu(chr(event.code), event.app)

    @handle(Keys.Backspace)
    def _(event):
        event.current_window.parent_menu()

    @handle(Keys.Enter)
    def _(event):
        event.current_window.select_menu(event.app)

    @handle(Keys.AltZ)
    @handle(Keys.ControlG)
    def _(event):
        event.current_window.hide()
        event.app.editor.pop_focus()

    return registry


class MenuItem(object):
    def __init__(self, name, shortcut, arg):
        assert isinstance(name, str) and name
        assert isinstance(shortcut, str) and shortcut
        assert callable(arg) or (isinstance(arg, list)
                and len(arg) > 0
                and all(isinstance(a, MenuItem) for a in arg))
        self.name = name + '[' + shortcut + ']'
        self.shortcut = shortcut
        self.parent = None
        self.action = None
        self.submenus = None

        if callable(arg):
            self.action = arg
        else:
            self.submenus = arg
            for menu in self.submenus:
                menu.parent = self

    @property
    def has_submenus(self):
        return self.action == None

    def __repr__(self):
        return 'Menu %r:%r' % (self.name, self.shortcut)

class Menu(PromptWindow):
    def __init__(self, *a, **ka):
        menus = ka.pop('menus', [])
	self.index_stack = [0]
        assert all(isinstance(menu, MenuItem) for menu in menus)
        PromptWindow.__init__(self, '', *a, **ka)

        self._root = MenuItem('root', 'r', menus)
        self.prompt_text = self.text

    @property
    def text(self):
        return self._root.submenus[self.index_stack[len(self.index_stack) - 1]].name

    def prev_menu(self):
	ind = self.index_stack[len(self.index_stack) - 1]
	if ind <= 0:
	    return

	self.index_stack[len(self.index_stack) - 1] = ind - 1

	self.prompt_text = self.text

    def next_menu(self, cycle = False):
	ind = self.index_stack[len(self.index_stack) - 1]
	if ind >= len(self._root.submenus) - 1 and not cycle:
	    return

	self.index_stack[len(self.index_stack) - 1] = (ind + 1) % len(self._root.submenus)

	self.prompt_text = self.text

    def enter_menu(self, key, app):
        matched_menu = None
        for menu in self._root.submenus:
            if menu.shortcut == key:
                matched_menu = menu
                break

        if matched_menu:
            if matched_menu.has_submenus:
                self._root = matched_menu
                self.index_stack.append(0)
                self.prompt_text = self.text
            else:
                app.editor.pop_focus()
                matched_menu.action(app)

    def select_menu(self, app):
        matched_menu = self._root.submenus[self.index_stack[len(self.index_stack) - 1]]
        if matched_menu:
            if matched_menu.has_submenus:
                self._root = matched_menu
                self.index_stack.append(0)
                self.prompt_text = self.text
            else:
                app.editor.pop_focus()
                matched_menu.action(app)

    def parent_menu(self):
        if self._root.parent is None:
            return
        self._root = self._root.parent
	self.index_stack.pop()
        self.prompt_text = self.text
