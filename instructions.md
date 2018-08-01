Dependencies
------------
    pip install six


References
----------

Creating an application
    examples/single_line_editor.py

custom bindings, message, error, confirmation, file selction, menu
    examples/binding.py

show busy (can be called from BufferBase or any child class)
    try:
        self.emit(EventType.STATUS_BUSY, 'msg...')
        // do some heavy work
    except:
        // log error
    finally:
        self.emit(EventType.STATUS_IDLE)

    NOTE: ALL event types are available in console/core/event_type.py

# get current window in a key handler
        current_window = e.current_window
            OR
        current_window = e.app.editor.current_window

        # where e is event passed to event handler(more details in console/core/event.py

        Also get current buffer associated with current window with 'current_window.buffer'

        NOTE see examples in console/bindings.py

Implementing a buffer
    create a new class which inherits from console.buffer_base.BufferBase and implement required methods

    see console/core/prompt_buffer.py

Logging
-------
    see console/core/buffer_base.py for example
     a file log.log is created when the application is run

Guidelines
----------

1. use arrow and first letter navigation
2. show 'top of item' and 'end of item'
3. show '1 of n', '2 of n' at the end of each list item

