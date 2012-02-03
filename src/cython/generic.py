import os.path


class DirectoryEntry(object):
    def __init__(self, name, path, type, **kwargs):
        self.__path = path
        self.__name = name
        self.__type = type
        self.__attrs = kwargs

    def __str__(self):
        return '<%s in %s, a %s, args %s>' % (self.__name,
                                              self.__path,
                                              self.__type,
                                              str(self.__attrs))
    def __repr__(self):
        return self.__str__()

    def is_directory(self):
        return self.__type == Directory

    def name(self):
        return self.__name

    def __cmp__(self, other):
        assert type(other) == DirectoryEntry
        if (self.__dict__ < other.__dict__):
            return -1
        elif (self.__dict__ > other.__dict__):
            return 1
        else:
            assert self.__dict__ == other.__dict__
            return 0


class FileType(object):
    def __init__(self, desc):
        self.__desc = desc

    def __str__(self):
        return self.__desc

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
