
class Position(object):
    def __init__(self, x = 0, y = 0):
        assert x >= 0
        assert y >= 0

        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        assert value >= 0
        self._x = value;

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        assert value >= 0
        self._y = value;

