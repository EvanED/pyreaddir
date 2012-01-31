import os.path


class DirectoryEntry(object):
    def __init__(self, name, path, type, **kwargs):
        self.__path = path
        self.__name = name
        self.__type = type
        self.__attrs = kwargs

    def __str__(self):
        return '<%s, a %s>' % (os.path.join(self.__path, self.__name),
                                    self.__type)
    def __repr__(self):
        return self.__str__()

    def is_directory(self):
        return self.__type == Directory

    def name(self):
        return self.__name


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
