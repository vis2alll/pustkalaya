from .keys import Key, Keys
from ..logger import logger

_logger = logger('key-binding')

class Binding(object):
    def __init__(self, key, handler, filter = None):
        assert isinstance(key, Key)
        assert callable(handler)
        assert filter is None or callable(filter) or isinstance(filter, bool)

        self.key = key
        self.handler = handler
        self.filter = filter
        self.window_type = None

    def call(self, event):
        self.handler(event)

    def __repr__(self):
        return 'Binding %r' % self.key


class Registry(object):
    def __init__(self, window_type = None):
        self._window_type = window_type
        self._key_bindings = []

    @property
    def window_type(self):
        return self._window_type

    def add_binding(self, key, **kwargs):
        "decorator for adding key binding to registry"

        if isinstance(key, (str, unicode)):
            key = Key(key, ord(key))

        filter = kwargs.pop('filter', None)

        assert isinstance(key, Key), 'key bindings should only be an instance of Key'

        def decorator(func):
            binding = Binding(key, func, filter = filter)
            binding.window_type = self.window_type
            self._key_bindings.append(binding)
            return func

        return decorator

    def remove_binding(self, handler):
        assert callable(handler)

        for binding in self._key_bindings:
            if binding.handler == handler:
                self._key_bindings.remove(k)
                return

    def remove_bindings(self, registry):
        assert isinstance(registry, Registry)

        for binding in registry._key_bindings:
            self._key_bindings.remove(binding)

    def get_binding_for_key(self, keycode, app):
        # try to find matching binding
        anykey_bindings = []
        bindings = []

        filtered_bindings = [binding for binding in self._key_bindings
                if (binding.window_type == None or
                isinstance(app.editor.current_window, binding.window_type))
                ]

        for binding in filtered_bindings:
            match_count = 0
            # _logger.debug('binding: %r' % binding)
            if binding.key.code == keycode:
                match_count += 1
                if binding.filter is not None:
                    if binding.filter(app) is True:
                        match_count += 1
                    else:
                        continue
                bindings.append((binding, match_count))
            if binding.key == Keys.Any:
                match_count += 1
                if binding.filter is not None:
                    if binding.filter(app) is True:
                        match_count += 1
                    else:
                        continue
                anykey_bindings.append((binding, match_count))

        # _logger.debug('bindings: %r' % bindings if len(bindings) > 0 else anykey_bindings)

        def getkey(tup):
            return tup[1]

        bindings.sort(key = getkey)
        anykey_bindings.sort(key = getkey)

        if len(bindings) == 0:
            return anykey_bindings[-1][0]

        # _logger.debug('bindings: %r' % bindings if len(bindings) > 0 else anykey_bindings)
        return bindings[-1][0]

    def handle(self, event):
        binding = self.get_binding_for_key(event.code, event.app)

        if binding is not None:
            event.key = binding.key
            binding.call(event)
        else:
            _logger.warn('unhandled keycode %d' % event.code)

class MergedRegistry(Registry):
    def __init__(self, registries):
        Registry.__init__(self)

        assert all(isinstance(registry, (Registry, MergedRegistry)) for registry in registries)

        for registry in registries:
            self._key_bindings.extend(registry._key_bindings)
