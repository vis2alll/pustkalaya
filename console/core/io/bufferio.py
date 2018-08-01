from .block import Block, BlockType
from ..bufferstate import BufferState

class Direction:
    UP = 'UP'
    PREVIOUS = 'PREVIOUS'
    DOWN = 'DOWN'
    NEXT = 'NEXT'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CURRENT = 'NONE'

class BlockMode:
    READ = 'Read'
    EDIT = 'Edit'

class BufferIO(object):
    TOP_OF_DOCUMENT = 'top of document'
    END_OF_DOCUMENT = 'end of document'

    def __init__(self, filename):
        assert filename is not None and len(filename) > 0
        self._filename = filename
        self._file = None
        self.state = BufferState.EDITING
        self._supports_block_editing = False
        self._supports_rich_text = False
        self._top_of_document = False # set to true when at the top or bottom
        self._end_of_document = False # set to true when at the top or bottom

    def _create_block(self, text, mode, ctype, selection = None):
        block = Block()

        block.text = text
        block.readonly = True if mode == BlockMode.READ else False
        block.type = ctype
        block.selection = selection

        return block


    @property
    def filename(self):
        return self._filename

    @property
    def table_mode(self):
        return self.state in [BufferState.TABLE_NAVIGATION, BufferState.TABLE_INFO]

    @property
    def supports_block_editing(self):
        return self._supports_block_editing

    @property
    def supports_rich_text(self):
        return self._supports_rich_text

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    @property
    def is_new_file(self):
        return False

    def current_block(self):
        raise NotImplementedError

    def next_block(self, direction, blocktype = None):
        raise NotImplementedError

    def first_block(self):
        raise NotImplementedError

    def last_block(self):
        raise NotImplementedError

    def preview_block(self, direction):
        raise NotImplementedError

    def update_block(self, text):
        pass

    def delete_block(self, direction = Direction.CURRENT):
        raise NotImplementedError

    def add_block(self, text):
        raise NotImplementedError

    def get_current_block_number(self):
        raise NotImplementedError

    def set_current_block_number(self, number):
        raise NotImplementedError

    # image
    def get_image_alt_text(self):
        raise NotImplementedError

    # table specific
    def table_info(self, infotype):
        raise NotImplementedError

    def insert_table(self, rows, columns):
        raise NotImplementedError

    def add_row(self):
        raise NotImplementedError

    def add_column(self):
        raise NotImplementedError

    def delete_row(self):
        raise NotImplementedError

    def delete_column(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def save_as(self, filepath):
        raise NotImplementedError

    def find(self, search_text, direction = Direction.NEXT):
        raise NotImplementedError

    def find_from_top(self, search_text):
        raise NotImplementedError

    def find_from_end(self, search_text):
        raise NotImplementedError

    def replace_all(self, search_text, replace_text):
        raise NotImplementedError

    # TOC
    def navigate_TOC(self, direction):
        raise NotImplementedError

    def jump_heading(self):
        raise NotImplementedError

    # clip board
    def selection_start(self, cursor):
        raise NotImplementedError

    def selection_end(self, cursor):
        raise NotImplementedError

    def selection_reset(self):
        pass
    def clipboard_copy(self):
        raise NotImplementedError

    def clipboard_cut(self):
        raise NotImplementedError

    def clipboard_paste(self, cursor):
        raise NotImplementedError

    def clipboard_delete(self):
        raise NotImplementedError

    # undo/redo
    def set_cursor_value_callback(self, cb):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


    def redo(self):
        return None


    def get_current_block_number(self):
        return 0

    def set_current_block_number(self, number):
        pass
