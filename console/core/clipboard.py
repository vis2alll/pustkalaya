from os import path
import tempfile

class ClipboardMimeType:
    XML = 'application/xml'
    PLAIN_TEXT = 'text/plain'

class Clipboard:
    FILE_PATH = path.join(tempfile.gettempdir(), 'clipboard')

    @staticmethod
    def put(text, mime_type = ClipboardMimeType.XML):
        assert text is not None

        textstr = text

        with open(Clipboard.FILE_PATH, 'w') as fh:
            fh.write(textstr.encode('utf8'))

    @staticmethod
    def get(mime_type = ClipboardMimeType.XML):
        if not path.exists(Clipboard.FILE_PATH):
            return None
        text = None
        with open(Clipboard.FILE_PATH, 'r') as fh:
            text = fh.read()

        return text
