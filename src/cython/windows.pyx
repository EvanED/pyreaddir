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
    BOOL FindNextFile(HANDLE hFindFile,
                      LPWIN32_FIND_DATAW lpFindFileData)

    
