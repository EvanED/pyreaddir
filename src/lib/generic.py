import os.path
import json
import collections

FileTypeBase = collections.namedtuple("FileTypeBase",
                                      ["description"])

class DirectoryEntry(object):
    def __init__(self, name, path, kind, **kwargs):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "kind", kind)

        for (k,v) in kwargs.iteritems():
            object.__setattr__(self, k, v)

        t = (name, path, kind, frozenset(kwargs.iteritems()))
        object.__setattr__(self, "_the_hash", hash(t))

    def extra_attrs(self):
        extras = {}
        d = self.dict_copy()
        for (k, v) in d.iteritems():
            if not k.startswith("_"):
                extras[k] = v
        return extras

    def __str__(self):
        return '<%s in %s, a %s, extras %s>' % (self.name,
                                                self.path,
                                                self.kind,
                                                self.extra_attrs())
    def __repr__(self):
        return self.__str__()

    def __setattr__(self, attr, value):
        raise TypeError("DirectoryEntry pretends to be immutable")

    def __getattribute__(self, attr):
        if attr == "__dict__":
            raise TypeError("DirectoryEntry pretends to be immutable")
        return super(DirectoryEntry, self).__getattribute__(attr)

    def is_directory(self):
        return self.kind == Directory

    def dict_copy(self, keep_privates=False):
        def keep(key):
            return key[0] != "_" or keep_privates
        d = object.__getattribute__(self, "__dict__")
        d = {k:v for (k,v) in d.iteritems() if keep(k)}
        return d

    def to_json(self, extras=None):
        if extras is None:
            extras={}
        extras.update(self.dict_copy())
        return json.dumps(extras)

    def __eq__(self, other):
        r = self.dict_copy() == other.dict_copy()
        return r

    def __ne__(self, other):
        r = self.dict_copy() != other.dict_copy()
        return r

    def __le__(self, other):
        a = sorted(self.dict_copy().iteritems())
        b = sorted(other.dict_copy().iteritems())
        return a <= b

    def __lt__(self, other):
        a = sorted(self.dict_copy().iteritems())
        b = sorted(other.dict_copy().iteritems())
        return a < b

    def __ge__(self, other):
        a = sorted(self.dict_copy().iteritems())
        b = sorted(other.dict_copy().iteritems())
        return a >= b
        
    def __gt__(self, other):
        a = sorted(self.dict_copy().iteritems())
        b = sorted(other.dict_copy().iteritems())
        return a > b

    def __hash__(self):
        return self._the_hash


class FileType(FileTypeBase):
    __slots__ = ()

    def __new__(self, desc):
        return FileTypeBase.__new__(self, desc)

    def __str__(self):
        return self.description

RegularFile  = FileType("regular file")
Directory    = FileType("directory")
SymbolicLink = FileType("symbolic link")
BlockDevice  = FileType("block device")
CharacterDevice = FileType("character device")
NamedPipe    = FileType("named pipe")
Socket       = FileType("socket")
Whiteout     = FileType("whiteout")
UnknownType  = FileType("unknown")

def _get_file_type_from_string(str):
    ty = globals()[str]
    #assert 
    return ty

