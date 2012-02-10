import os.path

import collections

DirectoryEntryBase = collections.namedtuple("DirectoryEntryBase",
                                            ["name", "path", "kind"])
FileTypeBase = collections.namedtuple("FileTypeBase",
                                      ["description"])

class DirectoryEntry(DirectoryEntryBase):
    __slots__ = ()

    def __new__(klass, name, path, kind, **kwargs):
        extras = sorted(kwargs.iteritems(), key=lambda pair: pair[0])
        keys = [k for (k,v) in extras]
        values = [v for (k,v) in extras]

        fields = ["name", "path", "kind", "private_base_"] + keys
        type_name = "__".join(keys)

        try:
            base = collections.namedtuple(type_name, fields)
        except ValueError as e:
            raise e

        return base.__new__(klass, name, path, base, kind, *values)

    def __str__(self):
        return '<%s in %s, a %s, args %s>' % (self.name,
                                              self.path,
                                              self.kind, '')
    def __repr__(self):
        return self.__str__()

    __iter__ = None

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
