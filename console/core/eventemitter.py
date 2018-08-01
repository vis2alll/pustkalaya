

class EventEmitter(object):
    def __init__(self):
        self._callbacks = {}

    def on(self, event_name, callback):
        assert event_name is not None and len(event_name) > 0
        assert callback is not None and callable(callable)

        if not event_name in self._callbacks.keys():
            self._callbacks[event_name] = []

        self._callbacks[event_name].append(callback)

    def emit(self, event_name, *a):
        assert event_name is not None and len(event_name) > 0

        if event_name in self._callbacks:
            for cb in self._callbacks[event_name]:
                cb(*a)

