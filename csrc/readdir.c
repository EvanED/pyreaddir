#include <Python.h>

#include <sys/types.h>
#include <dirent.h>


static PyObject*
py_opendir(PyObject* self, PyObject* args)
{
    // TODO:
    // - Deal with threads (i.e. insert Py_BEGIN_ALLOW_THREADS, but need to
    //   lock the buffer (c.f. PyBuffer?)
    // - Unicode?
    const char* dirname = 0;

    if (!PyArg_ParseTuple(args, "s", &dirname)) {
        return NULL;
    }

    DIR* directory = opendir(dirname);

    if (directory == NULL) {
        // TODO:
        // - Manpage says "For exceptions that involve a file system path
        //   (such as chdir() or unlink()), the exception instance will
        //   contain a third attribute, filename, which is the file name
        //   passed to the function."
        //
        // We might even want to store the directory name in the return value
        // from this function so that we can do that later.
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    assert(sizeof(unsigned long) == sizeof(directory));
    return Py_BuildValue("k", (unsigned long) directory);
}


static PyObject*
py_closedir(PyObject* self, PyObject* args)
{
    DIR* directory = 0;
    if (!PyArg_ParseTuple(args, "k", &directory)) {
        return NULL;
    }

    int closed = closedir(directory);

    if (closed != 0) {
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    Py_INCREF(Py_None);
    return Py_None;
}



static PyObject*
py_readdir(PyObject* self, PyObject* args)
{
    DIR* directory = 0;
    if (!PyArg_ParseTuple(args, "k", &directory)) {
        return NULL;
    }

    // TODO:
    // - Allow threads

    // Must clear errno, otherwise there's no way to tell whether readdir()
    // reached the end of the stream or if there was an error.
    errno = 0;
    struct dirent* entry = readdir(directory);

    if (entry == NULL) {
        if (errno == 0) {
            // No real error, just EOF
            Py_INCREF(Py_None);
            return Py_None;
        }
        else {
            return PyErr_SetFromErrno(PyExc_OSError);
        }
    }

    // TODO:
    // - Deal with case of no long long
    // - Really we want to pick the size of ino_t and such smartly
    //   and add assertions and such
    return Py_BuildValue("{s:k, s:k, s:H, s:B, s:s}",
                         "d_ino",    entry->d_ino,
                         "d_off",    entry->d_off,
                         "d_reclen", entry->d_reclen,
                         "d_type",   entry->d_type,
                         "d_name",   entry->d_name);
}


static PyMethodDef methods[] = {
    {"opendir",  py_opendir,  METH_VARARGS, "Open a directory."},
    {"readdir",  py_readdir,  METH_VARARGS, "Read a directory."},
    {"closedir", py_closedir, METH_VARARGS, "Close a directory."}
};


PyMODINIT_FUNC
initpyreaddir_c(void)
{
    (void) Py_InitModule("pyreaddir_c", methods);
}

