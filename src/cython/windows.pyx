cdef extern from "windows.h" nogil:

    ctypedef int DWORD
    ctypedef int HANDLE
    ctypedef void* LPVOID
    ctypedef int BOOL

    ctypedef int wchar_t
    ctypedef wchar_t WCHAR
    ctypedef wchar_t wchar_t_const "wchar_t const"
    ctypedef wchar_t_const* LPCWSTR

    ctypedef struct FILETIME:
        DWORD dwLowDateTime
        DWORD dwHighDateTime

    ctypedef struct WIN32_FIND_DATAW:
           DWORD dwFileAttributes
           FILETIME ftCreationTime
           FILETIME ftLastAccessTime
           FILETIME ftLastWriteTime
           DWORD nFileSizeHigh
           DWORD nFileSizeLow
           DWORD dwReserved0
           DWORD dwReserved1
           WCHAR  cFileName[260]
           WCHAR  cAlternateFileName[14]

    ctypedef WIN32_FIND_DATAW* LPWIN32_FIND_DATAW

    cdef enum FINDEX_INFO_LEVELS:
        FindExInfoStandard
        FindExInfoBasic # Needs Server 2008 R2 or Win 7

    cdef enum FINDEX_SEARCH_OPS:
        FindExSearchNameMatch
        FindExSearchLimitToDirectories
        FindExSearchLimitToDevices

    cdef enum: #???
        FIND_FIRST_EX_CASE_SENSITIVE
        FIND_FIRST_EX_LARGE_FETCH # Needs Server 2008 R2 or Win 7

    # HANDLE WINAPI FindFirstFileW(
    #   __in   LPCWSTR lpFileName,
    #   __out  LPWIN32_FIND_DATAW lpFindFileData
    # );
    HANDLE FindFirstFileW(LPCWSTR lpFileName,
                          LPWIN32_FIND_DATAW lpFindFileData)

    
    # HANDLE WINAPI FindFirstFileExW(
    #   __in        LPCWSTR lpFileName,
    #   __in        FINDEX_INFO_LEVELS fInfoLevelId,
    #   __out       LPVOID lpFindFileData,
    #   __in        FINDEX_SEARCH_OPS fSearchOp,
    #   __reserved  LPVOID lpSearchFilter,
    #   __in        DWORD dwAdditionalFlags
    # );
    HANDLE FindFirstFileExW(LPCWSTR lpFileName,
                            FINDEX_INFO_LEVELS fInfoLevelId,
                            LPVOID lpFindFileData,
                            FINDEX_SEARCH_OPS fSearchOp,
                            LPVOID lpSearchFilter,
                            DWORD dwAdditionalFlags)

    # BOOL WINAPI FindNextFile(
    #   __in   HANDLE hFindFile,
    #   __out  LPWIN32_FIND_DATA lpFindFileData
    # );
    BOOL FindNextFileW(HANDLE hFindFile,
                       LPWIN32_FIND_DATAW lpFindFileData)

    

# TODO: context manager
def readdir_gen(py_directory):
    py_directory = unicode(py_directory + '\\*')
    cdef wchar_t* directory = NULL #FIXME = py_directory
    cdef WIN32_FIND_DATAW result
    cdef HANDLE hFind
    #hFind = find_first_file_w(directory, presult)
    hFind = FindFirstFileExW(directory,
                             FindExInfoBasic,
                             &result,
                             FindExSearchNameMatch,
                             NULL,
                             FIND_FIRST_EX_LARGE_FETCH)
    
    if not hFind:
        raise Exception('Not found')

    while True:
        yield result
        res = FindNextFileW(hFind, &result)
        if not res:
            break

def FILETIME_to_datetime(FILETIME* ft):
    low = dwLowDateTime
    high = dwHighDateTime
    low = low << (sizeof(FILETIME) * 8)

    datetime.timedelta()

    ctypedef struct FILETIME:
        DWORD dwLowDateTime
        DWORD dwHighDateTime
