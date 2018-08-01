from .ui.editor import Editor
from .eventloop import EventLoop
from .core.keybinding import Registry, MergedRegistry
from .core.event import KeyEvent
from .logger import logger
from .bindings import load_basic_key_bindings, load_default_key_bindings
from .config import SCREEN_REFRESH_INTERVAL

from time import time

import curses

class Application(object):
    _logger = logger('app')
    def __init__(self,
            editor,
            registry = None):
        assert isinstance(editor, Editor)
        assert registry is None or isinstance(registry, MergedRegistry) or isinstance(registry, Registry)

        if registry is None:
            registry = MergedRegistry([
                load_default_key_bindings(),
                load_basic_key_bindings()
                ])

        self._editor = editor
        self._eventloop = EventLoop()
        self._registry = registry
        self._stopped = False       # set to true in Application .stop
        self._running = False

    def _start_application(self):
        """ initialize curses and start event loop
        """
        self._running = True
        prev = curr = time()

        while not self._stopped:
            event = self._eventloop.next(self._editor.current_window.curses_window)
            if event is not None:
                event.app = self

                self._registry.handle(event)
                prev = time() # reset timer

            curr = time()
            diff = int((curr - prev) * 1000)
            if (diff >= SCREEN_REFRESH_INTERVAL):
                self._refresh_screen()
                prev = curr



    def run(self):
        if not self._running and not self._stopped:
            self._start_application()

    def stop(self):
        self._stopped = True
        self._running = False

    @property
    def editor(self):
        return self._editor

    def _refresh_screen(self):
        if self._editor.is_dirty:
            self._editor.refresh()

