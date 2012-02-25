import tempfile
import os
import shutil

from generic import (DirectoryEntry, RegularFile, Directory,
                     SymbolicLink, NamedPipe)
from posix2 import readdir

test_tree = None

def setUpModule():
    global test_tree
    test_tree = set_up_workspace()

def tearDownModule():
    global test_tree
    remove_workspace(test_tree)


def set_up_workspace():
    def ino(f):
        return os.lstat(f).st_ino

    test_tree = {}
    test_tree["contents"] = set()

    root = tempfile.mkdtemp(prefix="pyreaddir.unittests.")
    test_tree["root dir"] = root
    
    # Create a normal file
    normal = os.path.join(root, "normal-file")
    f = open(normal, "w")
    f.close()

    test_tree["normal"] = DirectoryEntry("normal-file",
                                         root,
                                         RegularFile,
                                         inode=ino(normal))
    test_tree["contents"].add(test_tree["normal"])

    # Create a directory
    test_dir = os.path.join(root, "directory")
    os.mkdir(test_dir)

    test_tree["directory"] = DirectoryEntry("directory",
                                            root,
                                            Directory,
                                            inode=ino(test_dir))
    test_tree["contents"].add(test_tree["directory"])

    if True:
        # (Just indent to show structure)
        # Create a file *in* that directory:
        inner = os.path.join(test_dir, "inner-normal-file")
        f = open(inner, "w")
        f.close()
        test_tree["file in directory"] = DirectoryEntry("inner-normal-file",
                                                        test_dir,
                                                        RegularFile,
                                                        inode=ino(inner))

    # Create a named pipe
    fifo = os.path.join(root, "fifo")
    os.mkfifo(fifo)

    test_tree["named pipe"] = DirectoryEntry("fifo", root, NamedPipe, inode=ino(fifo))
    test_tree["contents"].add(test_tree["named pipe"])

    # Create devices?!

    # Create symlink to directory
    link_dir = os.path.join(root, "symlink-to-dir")
    os.symlink(test_dir, link_dir)

    test_tree["directory symlink"] = DirectoryEntry("symlink-to-dir",
                                                    root,
                                                    SymbolicLink,
                                                    inode=ino(link_dir))
    test_tree["contents"].add(test_tree["directory symlink"])

    # Create symlink to file
    link_file = os.path.join(root, "symlink-to-file")
    os.symlink(normal, link_file)

    test_tree["file symlink"] = DirectoryEntry("symlink-to-file",
                                               root,
                                               SymbolicLink,
                                               inode=ino(link_file))
    test_tree["contents"].add(test_tree["file symlink"])

    # Create socket?!

    # Create whiteout?!

    # Add . and ..
    test_tree["dot"] = DirectoryEntry(".", root, Directory, inode=ino(root))
    test_tree["contents"].add(test_tree["dot"])

    test_tree["dotdot"] = DirectoryEntry("..", root, Directory, inode=ino(os.path.join(root, "..")))
    test_tree["contents"].add(test_tree["dotdot"])

    return test_tree




def remove_workspace(workspace):
    root = workspace["root dir"]
    parent, name = os.path.split(root)

    assert name.startswith("pyreaddir.unittests.")

    shutil.rmtree(root)



import unittest
class TestBlah(unittest.TestCase):
    def test_blah(self):
        actual = list(readdir(test_tree["root dir"]))
        actual.sort()
        expected = list(test_tree["contents"])
        expected.sort()
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()

