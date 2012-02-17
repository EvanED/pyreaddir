import functools

@functools.total_ordering
class KeyValue(tuple):
    __slots__ = ()
    
    def __new__(klass, key, value):
        return tuple.__new__(klass, (key, value))

    def __eq__(self, other):
        if not isinstance(other, KeyValue):
            return False
        else:
            return self.key() == other.key()

    def __lt__(self, other):
        if not isinstance(other, KeyValue):
            raise TypeError("unorderable types")
        else:
            return self.key() < other.key()

    def __hash__(self):
        return hash(self.key())

    def key(self):
        return self[0]

    def value(self):
        return self[1]
