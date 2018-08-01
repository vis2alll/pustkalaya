
class Size(object):
    def __init__(self, width = 80, height = 25):
        assert width > 0
        assert height > 0

        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        assert value > 0
        self._width = value;

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        assert value > 0
        self._height = value;

