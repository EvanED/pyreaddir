import collections

_base = collections.namedtuple("_base", ["internal_keys", "internal_values"])

class frozendict(_base):
    __slots__ = ()

    def __new__(klass, mapping):
        sort = sorted(mapping.iteritems(), key=lambda pair: pair[0])
        keys = tuple(k for (k,v) in sort)
        values = tuple(v for (k,v) in sort)

        return _base.__new__(klass, keys, values)

    def __len__(self):
        return len(self.internal_keys)

    def __iter__(self):
        return iter(self.keys)

    def __contains__(self, value):
        return value in self.internal_keys
