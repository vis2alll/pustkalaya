from abc import ABCMeta, abstractmethod
from six import with_metaclass
from .range import InlineFormatRange
from ..logger import logger

import re
import traceback

_logger = logger('preprocessor')

class Preprocessor(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def to_processed(self, *a, **kw):
        """
        process text before displaying
        buffer : on which buffer we need to apply this preprocessor
        """
        raise NotImplementedError

    @abstractmethod
    def to_raw(self, *a, **kw):
        """
        unprocess text before saving
        buffer : on which buffer we need to apply this preprocessor
        """
        raise NotImplementedError

    @abstractmethod
    def to_processed_cursor(self, raw_cursor, *a):
        """
        return difference between raw and processed cursor
        """
        raise NotImplementedError

    @abstractmethod
    def to_raw_cursor(self, cursor, *a):
        """
        return difference between raw and processed cursor
        """
        raise NotImplementedError

class InlineFormatProcessors(Preprocessor):

    def __init__(self, formats):
        assert isinstance(formats, list)

        self._formats = formats
        # self._re_pariable = None
        # self._re_single = None
        self._re = None

    def to_processed(self, text):

        if not(self._re):
            format_regexs_pairable = ['(<%s>)(.*?)(</%s>)' % (f, f) for f in self._formats]
            format_regexs_single = ['(<%s_s>)(.*?)' % (f) for f in self._formats]
            # _logger.debug('format pattern: %r' % '|'.join(format_regexs_pairable))
            # _logger.debug('format pattern: %r' % '|'.join(format_regexs_single))

            self._re = re.compile('|'.join(format_regexs_single + format_regexs_pairable))

        format_ranges = []

        matches = self._re.finditer(text)
        offset = 0
        for match in matches:
            groups = match.groups()
            i = 0
            while groups[i] is None and i < len(groups):
                i += 1
            g1 = match.group(i + 1)
            g2 = match.group(i + 2)
            g3 = match.group(i + 3)

            # _logger.debug('groups: %r %r %r' % (g1, g2, g3))

            if g1 is None or g2 is None:
                continue

            if g3 is None:
                single = True
            else:
                single = False

            formatstr = match.group(i + 1)[1:-1]
            offset += len(match.group(i + 1))
            start = match.start(i + 2) - offset
            end = match.end(i + 2) - offset

            if not single:
                offset += len(match.group(i + 3))

            # _logger.debug('%r:start:%r, end:%r %r' % (match.group(i + 2), start, end, formatstr))

            if end > start:
                format_range = InlineFormatRange(start, end, formatstr, single)
                format_ranges.append(format_range)

            #_logger.debug('range: %r' % format_range)

        text = self._re.sub(self._replace_regex, text)

        return format_ranges, text

    def to_raw(self, text, format_ranges):
        offset = 0
        for fr in format_ranges:
            start_tag = '<' + fr.formatstr + '>'
            end_tag = '</' + fr.formatstr + '>'
            text = (text[:fr.start + offset] +
                    start_tag +
                    text[fr.start + offset:fr.end + offset] +
                    ('' if fr.single else end_tag) +
                    text[fr.end + offset:])

            offset += len(start_tag)
            offset += 0 if fr.single else len(end_tag)

        return text

    def to_processed_cursor(self, raw_cursor, format_ranges):
        diff = 0
        i = 0
        _logger.debug(' raw cursor %d' % raw_cursor)
        _logger.debug('format_ranges: %r' % format_ranges)

        if len(format_ranges) == 0:
            return 0

        len_before_cursor = 0
        while (i < len(format_ranges)):
            fr = format_ranges[i];
            start_tag_len = len('<' + fr.formatstr + '>')
            end_tag_len = 0 if fr.single else len('</' + fr.formatstr + '>')

            if ((fr.end - fr.start) + diff + start_tag_len + end_tag_len < raw_cursor):
                diff += start_tag_len
                diff += end_tag_len

                i += 1
            else:
                break

        _logger.debug('diff is : %d' % diff)

        if i < len(format_ranges):
            fr = format_ranges[i];

            start_tag_len = len('<' + fr.formatstr + '>')
            end_tag_len = 0 if fr.single else len('</' + fr.formatstr + '>')

            if fr.start + start_tag_len + diff <= raw_cursor:
                diff += start_tag_len

            if fr.end + end_tag_len + start_tag_len + diff <= raw_cursor:
                diff += end_tag_len

        _logger.debug('diff is : %d' % diff)

        return -diff

    def to_raw_cursor(self, cursor, format_ranges):
        diff = 0
        i = 0
        for fr in format_ranges:
            if fr.end <= cursor:
                diff += len('<' + fr.formatstr + '>')
                diff += 0 if fr.single else len('</' + fr.formatstr + '>')
                i += 1
            break

        if i < len(format_ranges) and format_ranges[i].start <= cursor:
            diff += len('<' + fr.formatstr + '>')

        return diff

    def _replace_regex(self, match):
        groups = match.groups()
        i = 0
        while groups[i] is None and i < len(groups):
            i += 1
        return match.group(i + 2)
