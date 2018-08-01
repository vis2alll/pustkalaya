from __future__ import unicode_literals

import curses

class Key(object):
    def __init__(self, name, code):

        #: Descriptive way of writing keys in configuration files. e.g. <C-A>
        #: for ``Control-A``.
        self.name = name
        self.code = code

    def __repr__(self):
        return '%s(%r:%d)' % (self.__class__.__name__, self.name, self.code)

class MetaKeys:
    ALT = 0x10000

class Keys(object):
    Escape = Key('<Escape>', 0x1b)

    # reference for control key combinations-
    # http://www.physics.udel.edu/~watson/scen103/ascii.html
    ControlA = Key('<C-A>', 0x01)
    ControlB = Key('<C-B>', 0x02)
    ControlC = Key('<C-C>', 0x03)
    ControlD = Key('<C-D>', 0x04)
    ControlE = Key('<C-E>', 0x05)
    ControlF = Key('<C-F>', 0x06)
    ControlG = Key('<C-G>', 0x07)
    ControlH = Key('<C-H>', 0x08)
    ControlI = Key('<C-I>', 0x09)  # Tab
    ControlJ = Key('<C-J>', 0x0a)  # Enter
    ControlK = Key('<C-K>', 0x0b)
    ControlL = Key('<C-L>', 0x0c)
    ControlM = Key('<C-M>', 0x0d)  # Enter
    ControlN = Key('<C-N>', 0x0e)
    ControlO = Key('<C-O>', 0x0f)
    ControlP = Key('<C-P>', 0x10)
    ControlQ = Key('<C-Q>', 0x11)
    ControlR = Key('<C-R>', 0x12)
    ControlS = Key('<C-S>', 0x13)
    ControlT = Key('<C-T>', 0x14)
    ControlU = Key('<C-U>', 0x15)
    ControlV = Key('<C-V>', 0x16)
    ControlW = Key('<C-W>', 0x17)
    ControlX = Key('<C-X>', 0x18)
    ControlY = Key('<C-Y>', 0x19)
    ControlZ = Key('<C-Z>', 0x1a)

    Alt0 = Key('<M-0>', MetaKeys.ALT | ord('0'))
    Alt1 = Key('<M-1>', MetaKeys.ALT | ord('1'))
    Alt2 = Key('<M-2>', MetaKeys.ALT | ord('2'))
    Alt3 = Key('<M-3>', MetaKeys.ALT | ord('3'))
    Alt4 = Key('<M-4>', MetaKeys.ALT | ord('4'))
    Alt5 = Key('<M-5>', MetaKeys.ALT | ord('5'))
    Alt6 = Key('<M-6>', MetaKeys.ALT | ord('6'))
    Alt7 = Key('<M-7>', MetaKeys.ALT | ord('7'))
    Alt8 = Key('<M-8>', MetaKeys.ALT | ord('8'))
    Alt9 = Key('<M-9>', MetaKeys.ALT | ord('9'))
    AltA = Key('<M-A>', MetaKeys.ALT | ord('A'))
    AltB = Key('<M-B>', MetaKeys.ALT | ord('B'))
    AltC = Key('<M-C>', MetaKeys.ALT | ord('C'))
    AltD = Key('<M-D>', MetaKeys.ALT | ord('D'))
    AltE = Key('<M-E>', MetaKeys.ALT | ord('E'))
    AltF = Key('<M-F>', MetaKeys.ALT | ord('F'))
    AltG = Key('<M-G>', MetaKeys.ALT | ord('G'))
    AltH = Key('<M-H>', MetaKeys.ALT | ord('H'))
    AltI = Key('<M-I>', MetaKeys.ALT | ord('I'))
    AltJ = Key('<M-J>', MetaKeys.ALT | ord('J'))
    AltK = Key('<M-K>', MetaKeys.ALT | ord('K'))
    AltL = Key('<M-L>', MetaKeys.ALT | ord('L'))
    AltM = Key('<M-M>', MetaKeys.ALT | ord('M'))
    AltN = Key('<M-N>', MetaKeys.ALT | ord('N'))
    AltO = Key('<M-O>', MetaKeys.ALT | ord('O'))
    AltP = Key('<M-P>', MetaKeys.ALT | ord('P'))
    AltQ = Key('<M-Q>', MetaKeys.ALT | ord('Q'))
    AltR = Key('<M-R>', MetaKeys.ALT | ord('R'))
    AltS = Key('<M-S>', MetaKeys.ALT | ord('S'))
    AltT = Key('<M-T>', MetaKeys.ALT | ord('T'))
    AltU = Key('<M-U>', MetaKeys.ALT | ord('U'))
    AltV = Key('<M-V>', MetaKeys.ALT | ord('V'))
    AltW = Key('<M-W>', MetaKeys.ALT | ord('W'))
    AltX = Key('<M-X>', MetaKeys.ALT | ord('X'))
    AltY = Key('<M-Y>', MetaKeys.ALT | ord('Y'))
    AltZ = Key('<M-Z>', MetaKeys.ALT | ord('Z'))

    #ControlSpace       = Key('<C-Space>')
    #ControlBackslash   = Key('<C-Backslash>')
    ControlSquareClose = Key('<C-SquareClose>', 0x1d)
    #ControlCircumflex  = Key('<C-Circumflex>')
    ControlUnderscore  = Key('<C-Underscore>', 0x1f)
    #ControlLeft        = Key('<C-Left>')
    #ControlRight       = Key('<C-Right>')
    #ControlUp          = Key('<C-Up>')
    #ControlDown        = Key('<C-Down>')

    Up          = Key('<Up>', curses.KEY_UP)
    Down        = Key('<Down>', curses.KEY_DOWN)
    Right       = Key('<Right>', curses.KEY_RIGHT)
    Left        = Key('<Left>', curses.KEY_LEFT)

    #ShiftLeft   = Key('<ShiftLeft>')
    #ShiftUp     = Key('<ShiftUp>')
    #ShiftDown   = Key('<ShiftDown>')
    #ShiftRight  = Key('<ShiftRight>')

    Home        = Key('<Home>', curses.KEY_HOME)
    End         = Key('<End>', curses.KEY_END)
    Delete      = Key('<Delete>', curses.KEY_DC)
    ShiftDelete = Key('<ShiftDelete>', curses.KEY_SDC)
    # ControlDelete = Key('<C-Delete>')
    PageUp      = Key('<PageUp>', curses.KEY_PPAGE)
    PageDown    = Key('<PageDown>', curses.KEY_NPAGE)
    BackTab     = Key('<BackTab>', curses.KEY_STAB)  # shift + tab
    Insert      = Key('<Insert>', curses.KEY_IC)
    Backspace   = Key('<Backspace>', curses.KEY_BACKSPACE)

    # Aliases.
    Tab         = ControlI
    Enter       = ControlJ
    AltEnter    = Key('<M-Enter>', MetaKeys.ALT | 0xa)
    AltF4       = Key('<M-F4>', MetaKeys.ALT | curses.KEY_F4)
    F1 = Key('<F1>', curses.KEY_F1)
    F2 = Key('<F2>', curses.KEY_F2)
    F3 = Key('<F3>', curses.KEY_F3)
    F4 = Key('<F4>', curses.KEY_F4)
    F5 = Key('<F5>', curses.KEY_F5)
    F6 = Key('<F6>', curses.KEY_F6)
    F7 = Key('<F7>', curses.KEY_F7)
    F8 = Key('<F8>', curses.KEY_F8)
    F9 = Key('<F9>', curses.KEY_F9)
    F10 = Key('<F10>', curses.KEY_F10)
    F11 = Key('<F11>', curses.KEY_F11)
    F12 = Key('<F12>', curses.KEY_F12)
    F13 = Key('<F13>', curses.KEY_F13)
    F14 = Key('<F14>', curses.KEY_F14)
    F15 = Key('<F15>', curses.KEY_F15)
    F16 = Key('<F16>', curses.KEY_F16)
    F17 = Key('<F17>', curses.KEY_F17)
    F18 = Key('<F18>', curses.KEY_F18)
    F19 = Key('<F19>', curses.KEY_F19)
    F20 = Key('<F20>', curses.KEY_F20)
    F21 = Key('<F21>', curses.KEY_F21)
    F22 = Key('<F22>', curses.KEY_F22)
    F23 = Key('<F23>', curses.KEY_F23)
    F24 = Key('<F24>', curses.KEY_F24)

    # Matches any key.
    Any = Key('<Any>', 0)

    # # Special
    # CPRResponse = Key('<Cursor-Position-Response>')
    # Vt100MouseEvent = Key('<Vt100-Mouse-Event>')
    # WindowsMouseEvent = Key('<Windows-Mouse-Event>')
    # BracketedPaste = Key('<Bracketed-Paste>')

    # # Key which is ignored. (The key binding for this key should not do
    # # anything.)
    # Ignore = Key('<Ignore>')
