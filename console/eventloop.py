import curses
from .logger import logger
from .core.event import KeyEvent
from .core.keys import Keys

import traceback

class EventLoop():
    _logger = logger('evnt-loop')
    def __init__(self):
        pass

    def next(self, window):
        try:
            alt = False
            ch = window.getch()
            if ch == -1:
                return None

            if ch == Keys.Escape.code:
                ch = window.getch()
                cA = ord('A')
                ca = ord('a')
                cz = ord('z')
                if ch != Keys.Escape.code:
                    if ch >= ca and ch <= cz:
                        ch = ch - ca + cA
                    alt = True

            keyevent = KeyEvent(ch, alt = alt)

            # EventLoop._logger.debug(keyevent)

            return keyevent
        except:
            EventLoop._logger.error(traceback.format_exc())
            return KeyEvent(Keys.ControlC.code)
