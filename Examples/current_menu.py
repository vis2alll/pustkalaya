

#from .base import Filter
from ...logger import logger
from sugamya_pustakalya import SugamyaPustakalya as sp
_logger = logger('current_menu')

 
class IsInMenu():
    def __init__(self, menu):
        self.menu = menu

    def __call__(self, app):
#        return app.editor.current_window.buffer.current_block_type == self._block_type
        return app ==self.menu

