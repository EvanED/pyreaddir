import collection
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
            return self.key() = other.key()

    def __lt__(self, other):
        if not isinstance(other, KeyValue):
            raise TypeError("unorderable types")
        else:
            return self.key() = other.key()

    def __hash__(self):
        return hash(self.key())

    def key(self):
        return self[0]

    def value(self):
        return self[1]

    

class frozendict(tuple):
    __slots__ = ()

    def __new__(klass, **kwargs):
        """Create a new frozen dict with the given mappings"""
        return __new__(klass, (kwargs,))

# __add__, __format__, __getattribute__, __getnewargs__,
# __getslice__, 

    def __contains__(self, item):
        return self[0].__contains__(item)

    def __eq__(self, other):
        # FIXME
        return self[0] == other[0]

    # __ge__, etc., __cmp__

    def __getitem__(self, item):
        return self[0][item]

    # __hash__

    def __iter__(self):
        return iter(self[0])

    
