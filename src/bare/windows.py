import generic

from ctypes import *
import ctypes
import ctypes.wintypes as win


_dword_type = win.DWORD

class FILETIME(Structure):
    """typedef struct _FILETIME {
           DWORD dwLowDateTime;
           DWORD dwHighDateTime;
       } FILETIME, *PFILETIME;"""

    _fields_ = [("dwLowDateTime",  _dword_type),
                ("dwHighDateTime", _dword_type)
                ]


class WIN32_FIND_DATAW(Structure):
    """typedef struct _WIN32_FIND_DATAW {
           DWORD dwFileAttributes;
           FILETIME ftCreationTime;
           FILETIME ftLastAccessTime;
           FILETIME ftLastWriteTime;
           DWORD nFileSizeHigh;
           DWORD nFileSizeLow;
           DWORD dwReserved0;
           DWORD dwReserved1;
           WCHAR  cFileName[ 260 ];
           WCHAR  cAlternateFileName[ 14 ];
       } WIN32_FIND_DATAW;"""

    _fields_ = [("dwFileAttributes",   _dword_type),
                ("ftCreationTime",     FILETIME),
                ("ftLastAccessTime",   FILETIME),
                ("ftLastWriteTime",    FILETIME),
                ("nFileSizeHigh",      _dword_type),
                ("nFileSizeLow",       _dword_type),
                ("dwReserved0",        _dword_type),
                ("dwReserved1",        _dword_type),
                ("cFileName",          c_wchar * 260),
                ("cAlternateFileName", c_wchar * 14)
                ]


# HANDLE WINAPI FindFirstFileW(
#   __in   LPCWSTR lpFileName,
#   __out  LPWIN32_FIND_DATAW lpFindFileData
# );

find_first_file_w = ctypes.windll.kernel32.FindFirstFileW

find_first_file_w.argtypes = [win.LPCWSTR, POINTER(WIN32_FIND_DATAW)]
find_first_file_w.restype = win.HANDLE

# BOOL WINAPI FindNextFile(
#   __in   HANDLE hFindFile,
#   __out  LPWIN32_FIND_DATA lpFindFileData
# );

find_next_file_w = ctypes.windll.kernel32.FindNextFileW

find_next_file_w.argtypes = [win.HANDLE, POINTER(WIN32_FIND_DATAW)]
find_next_file_w.restype = win.BOOL


# TODO: context manager
def readdir_gen(directory):
    directory = unicode(directory + '\\*')
    result = WIN32_FIND_DATAW()
    presult = pointer(result)
    hFind = find_first_file_w(directory, presult)
    
    if not hFind:
        raise Exception('Not found')

    while True:
        yield presult.contents
        res = find_next_file_w(hFind, presult)
        if not res:
            break


FILE_ATTRIBUTE_ARCHIVE    = 0x20
FILE_ATTRIBUTE_COMPRESSED = 0x800
FILE_ATTRIBUTE_DEVICE     = 0x40
FILE_ATTRIBUTE_DIRECTORY  = 0x10
FILE_ATTRIBUTE_ENCRYPTED  = 0x4000
FILE_ATTRIBUTE_HIDDEN     = 0x2
FILE_ATTRIBUTE_NORMAL     = 0x80
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x2000
FILE_ATTRIBUTE_OFFLINE    = 0x1000
FILE_ATTRIBUTE_READONLY   = 0x1
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
FILE_ATTRIBUTE_SPARSE_FILE = 0x200
FILE_ATTRIBUTE_SYSTEM     = 0x4
FILE_ATTRIBUTE_TEMPORARY  = 0x100
FILE_ATTRIBUTE_VIRTUAL    = 0x10000

IO_REPARSE_TAG_DFS     = 0x8000000A
IO_REPARSE_TAG_DFSR    = 0x80000012
IO_REPARSE_TAG_HSM     = 0xC0000004
IO_REPARSE_TAG_HSM2    = 0x80000006
IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003
IO_REPARSE_TAG_SIS     = 0x80000007
IO_REPARSE_TAG_SYMLINK = 0xA000000C


def get_generic_type(dirent):
    attrs = dirent.dwFileAttributes
    if attrs & FILE_ATTRIBUTE_DIRECTORY:
        return generic.Directory
    if attrs & FILE_ATTRIBUTE_DEVICE:
        return generic.BlockDevice  #TODO?
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
        tag = dirent.dwReserved0
        if tag == IO_REPARSE_TAG_SYMLINK:
            return generic.SymbolicLink
        if tag == IO_REPARSE_TAG_MOUNT_POINT:
            return generic.Directory
        return generic.UnknownType
    # named pipes and sockets
    if attrs & FILE_ATTRIBUTE_VIRTUAL:
        return generic.UnknownType
    return generic.RegularFile
    
    
def genericize(dirent):
    return generic.DirectoryEntry(dirent.cFileName,
                                  get_generic_type(dirent),
                                  -1)

def listdir(dirname):
    return (genericize(entry) for entry in readdir_gen(dirname))
