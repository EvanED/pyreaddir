import os.path

import collections

DirectoryEntryBase = collections.namedtuple("DirectoryEntryBase",
                                            ["path", "name", "type"])
FileTypeBase = collections.namedtuple("FileTypeBase",
                                      ["description"])

class DirectoryEntry(DirectoryEntryBase):
    __slots__ = ()

    def __new__(self, name, path, type, **kwargs):
        return DirectoryEntryBase.__new__(self, name, path, type)
        #self.__attrs = kwargs

    def __str__(self):
        return '<%s in %s, a %s, args %s>' % (self.__name,
                                              self.__path,
                                              self.__type,
                                              str(self.__attrs))
    def __repr__(self):
        return self.__str__()

    def is_directory(self):
        return self.type == Directory


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
