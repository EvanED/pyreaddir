import os.path

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
        for (k, v) in self.__dict__.iteritems():
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

    __setattr__ = None

    def is_directory(self):
        return self.kind == Directory


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

print RegularFile
print DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)
