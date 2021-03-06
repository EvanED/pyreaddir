NOT ALL OF THIS IS IMPLEMENTED YET. (This file was originally called
plan.txt but I renamed it for GitHub's benefit.)


readdir(directory, glob="*", extra_filters=[],
        [transaction=None, limit_information=None])

    Lists all files in directory that match glob and all filters in
    extra_filters. The glob pattern uses the syntax of the fnmatch
    module, which supports *, ?, and [...] and [!...] character
    classes. (On POSIX, this will be emulated by just filtering the
    resulting list of files. On Windows, the * and ? wildcards can be
    dealt with by the system, but character classes will have to be
    replaced by ? and then filtered later.)

    extra_filters is a sequence of predicates which will be called
    with each file; if a predicate returns false, that file will not
    be returned. The library will have a pre-defined filter which will
    check whether a file is a directory; on Windows, readdir will
    detect that filter and pass that request down to the file system.

    transaction is only available on Windows and will result in a call
    to the transacted version with the given handle.

    limit_information is also only avaliable on Windows and can be any
    one of a predefined list of values which will get passed down to
    Windows. The fields which have no meaning will be dropped from the
    iterator's items.


readdir returns a sequence, each item of which will be an object with
the following attributes:

    name: the file name

    kind, available on most systems: one of a set of predefined
    values: regular file, directory, device (on POSIX, an attribute of
    the kind field itself will indicate block or character), and
    symbol link (on Windows, an attribute of the kind field itself
    will indicate the type of symlink) will be available across all
    kind-capable systems. On POSIX, other options are FIFO, socket,
    and unknown. On Windows, reparse point. (Reparse points with the
    SYMLINK tag will count as a symlink. Other tags will be available
    as an attribute of kind itself.)

    inode, available on POSIX.

    d_off, available on some POSIX.

    attributes, available on Windows. An object with a bunch of
    boolean fields for: hidden, system, archive, read-only,
    compressed, encrypted, indexed, offline, sparse, temporary,
    virtual.

    creation_time, access_time, modification_time, available on
    Windows. Each is adatetime. (Exceptions: if the file system
    doesn't support this, then Windows sets the field to 0; I will
    omit it this attribute from the resulting object in that case.)

    size, available on Windows. The size of the file.

    short_name, available on Windows. An 8.3 filename. (Exception:
    this attribute will be omitted if it is not set in the result from
    Windows.)
