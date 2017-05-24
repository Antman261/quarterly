import arrow
from datetime import datetime


class Quarter(arrow.Arrow):
    """
    Allows consumer to interact with quarters while maintaining datetime interface.
    """

    def __init__(self, *args, **kwargs):
        """
        An instance of Quarterly is an Arrow range (two Arrow instances).

        Quarterly implements Iterator Type.

        Returns current quarter.
        """
        if isinstance(Quarter, type):
            super(Quarter, self).__init__(*args, **kwargs)
        else:
            arrow.Arrow.__init__(self, *args, **kwargs)
        self.start, self.end = arrow.Arrow(*args, **kwargs).span('quarter')

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.__str__())

    def __str__(self):
        return '%s - %s' % (self.start.isoformat(), self.end.isoformat())

    def __eq__(self, other):
        if isinstance(other, (Quarter, arrow.Arrow)):
            return self.quarter == other.quarter

        if not isinstance(other, (arrow.Arrow, datetime)):
            return False

        return self._datetime == self._get_datetime(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, (Quarter, arrow.Arrow)):
            return self.quarter > other.quarter

        if not isinstance(other, (arrow.Arrow, datetime)):
            self._cmperror(other)

        return self._datetime > self._get_datetime(other)

    def __ge__(self, other):
        if isinstance(other, (Quarter, arrow.Arrow)):
            return self.quarter >= other.quarter

        if not isinstance(other, (arrow.Arrow, datetime)):
            self._cmperror(other)

        return self._datetime >= self._get_datetime(other)

    def __lt__(self, other):
        if isinstance(other, (Quarter, arrow.Arrow)):
            return self.quarter < other.quarter

        if not isinstance(other, (arrow.Arrow, datetime)):
            self._cmperror(other)

        return self._datetime < self._get_datetime(other)

    def __le__(self, other):
        if isinstance(other, (Quarter, arrow.Arrow)):
            return self.quarter <= other.quarter

        if not isinstance(other, (arrow.Arrow, datetime)):
            self._cmperror(other)

        return self._datetime <= self._get_datetime(other)

    def __iter__(self):
        return self

    def __next__(self):
        return QuarterFactory().get(self.start.replace(months=+self._MONTHS_PER_QUARTER))

    next = __next__  # Alias for python2.7

    def prev(self):
        return QuarterFactory().get(self.start.replace(months=-self._MONTHS_PER_QUARTER))

    @property
    def days(self):
        return len(self.span_range('day', self.start, self.end))

    @property
    def remaining(self):
        return len(self.span_range('day', self, self.end))

    @property
    def elapsed(self):
        """The number of complete days since the start of the quarter."""
        return len(self.span_range('day', self.start, self))-1  # Do not include today


class QuarterFactory(arrow.ArrowFactory):
    def __init__(self, type=Quarter):
        self.type = type
