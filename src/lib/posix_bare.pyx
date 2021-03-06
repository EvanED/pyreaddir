cdef extern from "errno.h":
    int errno

cdef extern from "dirent.h":
    ctypedef int ino_t
    ctypedef int off_t
    ctypedef char* const_char_t "const char*"

    ctypedef struct DIR:
        pass

    cdef struct dirent:
        ino_t d_ino
        off_t d_off
        unsigned short d_reclen
        unsigned char  d_type
        char           d_name[256]

    DIR* opendir(const_char_t name)
    dirent* readdir(DIR* directory)
    int closedir(DIR* directory)


    enum:
        DT_UNKNOWN
        DT_FIFO
        DT_CHR
        DT_DIR
        DT_BLK
        DT_REG
        DT_LNK
        DT_SOCK
        DT_WHT

cdef set_errno(int a):
    global errno
    errno = 0

cdef int get_errno():
    return errno

cdef genericize_dirent(dirent* dirent):
    return {'name': dirent.d_name,
            'type': genericize_d_type(dirent.d_type),
            'inode': dirent.d_ino}

cdef genericize_d_type(int type):
    if type == DT_UNKNOWN:
        return 'UnknownType'
    if type == DT_FIFO:
        return 'NamedPipe'
    if type == DT_CHR:
        return 'CharacterDevice'
    if type == DT_DIR:
        return 'Directory'
    if type == DT_BLK:
        return 'Blockdevice'
    if type == DT_REG:
        return 'RegularFile'
    if type == DT_LNK:
        return 'SymbolicLink'
    if type == DT_SOCK:
        return 'Socket'
    if type == DT_WHT:
        return 'Whiteout'
    return 'ReallyUnknown'
    

cdef class DirectoryIterator:
    cdef DIR* handle

    def __cinit__(self, dir_name):
        self.handle = opendir(dir_name)
        if self.handle == NULL:
            raise Exception(get_errno())

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.handle == NULL:
            raise Exception()
        set_errno(0)
        cdef dirent* entry = readdir(self.handle)
        if entry == NULL:
            if get_errno() == 0: 
                raise StopIteration()
            else:
                raise Exception(get_errno())
        else:
            return genericize_dirent(entry)

    def close(self):
        if self.handle != NULL:
            closedir(self.handle)
            self.handle = NULL

