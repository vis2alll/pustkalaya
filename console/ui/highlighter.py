from abc import ABCMeta, abstractmethod
from six import with_metaclass
from ..logger import logger
from ..core.range import Range

import curses

_logger = logger('highlighter')

class Highlighter(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def activate(self, window):
        raise NotImplementedError

    def highlight_range(self, window, linecounts, format_range, style):
        start = format_range.start
        end = format_range.end

        length = format_range.end - format_range.start

        while length > 0:
            row, col = window.row_column_from_cursor(start)

            length_to_paint = min(length, linecounts[row] - start)

            # _logger.debug('[row, col, length] : [%d, %d %d]' % (row, col, length_to_paint))
            window.highlight(style, row, col, length_to_paint)
            start += length_to_paint
            length -= length_to_paint

class InlineFormatHighlighter(Highlighter):

    def __init__(self, formats):
        assert isinstance(formats, list)

        self._styles = {}
        for f in formats:
            attr = curses.A_NORMAL
            if 'b' in f:
                attr |= curses.A_BOLD
            if 'i' in f and 'u' in f:
                attr |= curses.color_pair(3)
            elif 'i' in f:
                attr = curses.color_pair(1)
            elif 'u' in f:
                attr = curses.color_pair(2)

            self._styles[f] = attr
            self._styles[f + '_s'] = attr

    def activate(self, window):
        format_ranges = window.buffer.format_ranges
        lines = window.lines

        linecounts = []
        count = 0
        for line in lines:
            count += len(line)
            linecounts.append(count)

        for fr in format_ranges:
            if fr.end <= fr.start:
                continue
            self.highlight_range(window, linecounts, fr, self._styles[fr.formatstr])


class SelectionHighlighter(Highlighter):

    def __init__(self):
        self._style = curses.A_REVERSE

    def activate(self, window):
        selection_range = window.buffer.selection_range
        # _logger.debug('selection %r' % selection_range)
        if selection_range is None:
            return

        lines = window.lines
        newlines = window.newlines

        linecounts = []
        count = 0
        rows = len(lines)
        row = 0
        while row < rows:
            count += len(lines[row])
            count += 1 if newlines[row] else 0
            linecounts.append(count)
            row += 1

        self.highlight_range(window, linecounts, selection_range, self._style)
