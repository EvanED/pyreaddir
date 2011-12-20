from ctypes import *
import generic

class DIR(Structure):
    pass

class DIRENT(Structure):
    """struct dirent {
           // on my machine, both ino_t and off_t are 8 bytes, so c_ulonglong
           ino_t          d_ino;       /* inode number */
           off_t          d_off;       /* offset to the next dirent */
           // c_ushort
           unsigned short d_reclen;    /* length of this record */
           // c_ubyte
           unsigned char  d_type;      /* type of file */
           // 
           char           d_name[256]; /* filename */
        };"""

    _fields_ = [("d_ino",    c_ulonglong),
                ("d_off",    c_ulonglong),
                ("d_reclen", c_ushort),
                ("d_type",   c_ubyte),
                ("d_name",   c_char * 256)]

    def __str__(self):
        global dt_type_values
        return '<' + self.d_name + ', type: ' + dt_type_values[self.d_type][0] + '>'

_libc = CDLL("libc.so.6", use_errno=True)

# DIR *opendir(const char *name);
_libc.opendir.argtypes = [c_char_p]
_libc.opendir.restype = POINTER(DIR)

# struct dirent *readdir(DIR *dir);
_libc.readdir.argtypes = [POINTER(DIR)]
_libc.readdir.restype = POINTER(DIRENT)

# int closedir(DIR *dir);
_libc.closedir.argtypes = [POINTER(DIR)]


opendir = _libc.opendir
readdir = _libc.readdir
closedir = _libc.closedir


dt_type_values = {
    0:  ("DT_UNKNOWN", generic.UnknownType),
    1:  ("DT_FIFO", generic.NamedPipe),
    2:  ("DT_CHR",  generic.CharacterDevice),
    4:  ("DT_DIR",  generic.Directory),
    6:  ("DT_BLK",  generic.BlockDevice),
    8:  ("DT_REG",  generic.RegularFile),
    10: ("DT_LNK",  generic.SymbolicLink),
    12: ("DT_SOCK", generic.Socket),
    14: ("DT_WHT",  generic.Whiteout)
    }


#example code from opengroup
"""
dirp = opendir(".");

while (dirp) {
    errno = 0;
    if ((dp = readdir(dirp)) != NULL) {
        if (strcmp(dp->d_name, name) == 0) {
            closedir(dirp);
            return FOUND;
        }
    } else {
        if (errno == 0) {
            closedir(dirp);
            return NOT_FOUND;
        }
        closedir(dirp);
        return READ_ERROR;
    }
}
"""

# TODO: context manager
def readdir_gen(directory):
    dirp = opendir(directory)
    if dirp == None:
        raise Exception(get_errno())

    while True:
        dirent = readdir(dirp)

        if not dirent:
            if get_errno() == 0:
                closedir(dirp)
                return
            else:
                raise Exception(get_errno())

        #print dirent.contents
        yield dirent.contents

    
def genericize(path, dirent):
    return generic.DirectoryEntry(dirent.d_name,
                                  path,
                                  dt_type_values[dirent.d_type][1],
                                  dirent.d_ino)

def listdir(dirname):
    return (genericize(dirname, entry) for entry in readdir_gen(dirname))
