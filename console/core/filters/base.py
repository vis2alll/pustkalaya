from abc import ABCMeta, abstractmethod
from six import with_metaclass

class Filter(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def __call__(self, *a, **kw):
        """
        actual call to evavulate the filter
        """
        return True

class OrFilter(Filter):
    def __init__(self, *filters):
        assert all(isinstance(filter, Filter) for filter in filters)

        self._filters = filters

    def __call__(self, *a, **kw):
        return any(filter(*a, **kw) for filter in self._filters)

class AndFilter(Filter):
    def __init__(self, *filters):
        assert all(isinstance(filter, Filter) for filter in filters)

        self._filters = filters

    def __call__(self, *a, **kw):
        return all(filter(*a, **kw) for filter in self._filters)

class NotFilter(Filter):
    def __init__(self, filter):
        assert isinstance(filter, Filter)

        self._filter = filter

    def __call__(self, *a, **kw):
        return not self._filter(*a, **kw)
