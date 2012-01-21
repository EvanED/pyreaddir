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


cdef readdir_gen(directory):
    DIR* dirp = opendir(directory)
    if dirp == NULL:
        raise Exception(get_errno())

    while True:
        dirent* dirent = readdir(dirp)

        if not dirent:
            if get_errno() == 0:
                closedir(dirp)
                return
            else:
                raise Exception(get_errno())

        #print dirent.contents
        yield dirent.contents
