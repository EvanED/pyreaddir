
import windows as platform
import os.path
import generic


_listdir = platform.listdir


DirectoryEntry = generic.DirectoryEntry
FileType = generic.FileType
RegularFile  = generic.RegularFile
Directory    = generic.Directory
SymbolicLink = generic.SymbolicLink
BlockDevice  = generic.BlockDevice
CharacterDevice = generic.CharacterDevice
NamedPipe    = generic.NamedPipe
Socket       = generic.Socket
Whiteout     = generic.Whiteout
UnknownType  = generic.UnknownType


def directory_contents(directory, recursive=False):
    if not recursive:
        return _listdir(directory)

    else:
        def rec_helper(prefix, this_dir):
            dirs = []
            this_path = os.path.join(prefix, this_dir)
            lst = _listdir(this_path)
            for entry in lst:
                if entry.is_directory() and entry.name() not in ['.', '..']:
                    dirs.append(entry.name())
                yield entry

            for subdir in dirs:
                lst = rec_helper(this_path, subdir)
                for entry in lst:
                    yield entry

        return rec_helper('', directory)

