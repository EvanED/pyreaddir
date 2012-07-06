import generic
import posix_wrapper

DirectoryEntry = generic.DirectoryEntry

FileType = generic.FileType

RegularFile = generic.RegularFile
Directory = generic.Directory
SymbolicLink = generic.SymbolicLink
BlockDevice = generic.BlockDevice
CharacterDevice = generic.CharacterDevice
NamedPipe = generic.NamedPipe
Socket = generic.Socket
Whiteout = generic.Whiteout
UnknownType = generic.UnknownType

readdir = posix_wrapper.readdir
