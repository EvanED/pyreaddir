cdef class frozendict:
    cdef object d

    def __cinit__(self, **kwargs):
        d = dict(kwargs)
