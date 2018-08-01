class BlockType(object):
    PARAGRAPH = 'Paragraph'
    IMAGE = 'IMAGE'
    TABLE = 'TABLE'
    ALTTEXT = 'ALTTEXT'
    HEADING = 'Heading'
    LIST     = 'List'
    OBJECT = 'Object'
    PAGE_BREAK = 'PageBreak'
    FIRST_BLOCK = 'Home'
    LAST_BLOCK = 'End'
    TABLE_CELL = 'TableCell'

def issameblocktype(type1, type2):
    assert type1 is not None and type2 is not None

    return type1.lower() == type2.lower()

class Block(object):
    def __init__(self):
        self._text = ''
        self._type = BlockType.PARAGRAPH
        self._readonly = False
        self.modified = False
        self.is_new = False
        self.format_ranges = [] # holds range of inline formatted texts
        self.selection = None
        self.cursor = None

    def __repr__(self):
        return '[Block]: readonly: %r, mode: %r, text: %r' % (self.readonly, self.type, self.text)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value == 'Image':
            self._type = BlockType.IMAGE
        elif value == 'Table':
            self._type = BlockType.TABLE
        elif value == 'Object':
            self._type = BlockType.OBJECT
        # elif value is not None and value.startswith('lvl'):
        #     self._type = BlockType.LIST
        else:
            self._type = BlockType.PARAGRAPH

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value

    @property
    def can_edit(self):
        return self.type in [BlockType.PARAGRAPH, BlockType.LIST] and not self.readonly

