from keys import MetaKeys

class KeyEvent():
    def __init__(self, code, window = None, app = None, alt = False):
        self.code = code | (MetaKeys.ALT if alt else 0) # event code received from terminal
        self.key = None                                 # instance of Key console.core.kyes
        self.app = app                                  # instance of Application console.Application
        self.alt = alt                                  # whether alt key was pressed

    def __repr__(self):
        return 'KeyEvent: code: %r, key: %r, alt: %r' % (self.code, self.key, self.alt)

    @property
    def current_window(self):
        return self.app.editor.current_window
