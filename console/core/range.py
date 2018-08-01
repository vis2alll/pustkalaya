class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Range: [%r %r]' % (self.start, self.end)

class InlineFormatRange(Range):
    def __init__(self, start, end, formatstr, single = False):
        Range.__init__(self, start, end)

        assert len(formatstr) > 0
        self.formatstr = formatstr
        self.single = single

    def __repr__(self):
        return 'start,end,formatstr: %r,%r,%r' % (self.start, self.end, self.formatstr)

    def split(self, pos):
        offset = pos - self.start

        first = InlineFormatRange(self.start, self.start + offset, self.formatstr)
        last = InlineFormatRange(self.start + offset, self.end, self.formatstr)

        return first, last

