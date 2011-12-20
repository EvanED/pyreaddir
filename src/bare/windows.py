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
        yield presult.contents.cFileName
        res = find_next_file_w(hFind, presult)
        if not res:
            break


    
def genericize(dirent):
    return generic.DirectoryEntry(dirent.cFileName,
                                  dt_type_values[dirent.d_type][1],
                                  dirent.d_ino)

def listdir(dirname):
    return (genericize(entry) for entry in readdir_gen(dirname))
