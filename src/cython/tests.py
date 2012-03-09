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
    test_tree["contents: extra recursive"] = set()
    test_tree["contents: normal-?-file"] = set()
    test_tree["contents: normal*"] = set()

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
    test_tree["contents: normal*"].add(test_tree["normal"])

    # Make more more files, used for glob tests
    normal = os.path.join(root, "normal-1-file")
    f = open(normal, "w")
    f.close()
    test_tree["normal-1"] = DirectoryEntry("normal-1-file",
                                           root,
                                           RegularFile,
                                           inode=ino(normal))
    test_tree["contents"].add(test_tree["normal-1"])
    test_tree["contents: normal-?-file"].add(test_tree["normal-1"])
    test_tree["contents: normal*"].add(test_tree["normal-1"])


    normal = os.path.join(root, "normal-2-file")
    f = open(normal, "w")
    f.close()
    test_tree["normal-2"] = DirectoryEntry("normal-2-file",
                                           root,
                                           RegularFile,
                                           inode=ino(normal))
    test_tree["contents"].add(test_tree["normal-2"])
    test_tree["contents: normal-?-file"].add(test_tree["normal-2"])
    test_tree["contents: normal*"].add(test_tree["normal-2"])

    normal = os.path.join(root, ".hidden-file")
    f = open(normal, "w")
    f.close()
    test_tree["hidden"] = DirectoryEntry(".hidden-file",
                                         root,
                                         RegularFile,
                                         inode=ino(normal))
    test_tree["contents"].add(test_tree["hidden"])


    # Create a directory
    test_dir = os.path.join(root, "directory")
    os.mkdir(test_dir)

    test_tree["directory"] = DirectoryEntry("directory",
                                            root,
                                            Directory,
                                            inode=ino(test_dir))
    test_tree["contents"].add(test_tree["directory"])

    test_dir = os.path.join(root, "normal-3-file") # It lies
    os.mkdir(test_dir)

    test_tree["directory-3"] = DirectoryEntry("normal-3-file",
                                              root,
                                              Directory,
                                              inode=ino(test_dir))
    test_tree["contents"].add(test_tree["directory-3"])
    test_tree["contents: normal-?-file"].add(test_tree["directory-3"])
    test_tree["contents: normal*"].add(test_tree["directory-3"])


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
        test_tree["contents: extra recursive"].add(test_tree["file in directory"])

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
    def test_basic_readdir(self):
        actual = list(readdir(test_tree["root dir"]))
        actual.sort()
        expected = list(test_tree["contents"])
        expected.sort()
        self.assertEqual(actual, expected)

    def test_readdir_with_star_glob(self):
        actual = list(readdir(test_tree["root dir"], glob="*"))
        actual.sort()
        expected = list(test_tree["contents"])
        expected.sort()
        self.assertEqual(actual, expected)

    def test_readdir_with_normal_q_file_glob(self):
        actual = list(readdir(test_tree["root dir"], glob="normal-?-file"))
        actual.sort()
        expected = list(test_tree["contents: normal-?-file"])
        expected.sort()
        self.assertEqual(actual, expected)

    def test_readdir_with_normal_star_glob(self):
        actual = list(readdir(test_tree["root dir"], glob="normal*"))
        actual.sort()
        expected = list(test_tree["contents: normal*"])
        expected.sort()
        self.assertEqual(actual, expected)

    @unittest.expectedFailure
    def test_recursive_readdir(self):
        actual = list(readdir(test_tree["root dir"], recursive=True))
        actual.sort()
        expected = (list(test_tree["contents"])
                    + list(test_tree["contents: extra recursive"]))
        expected.sort()
        self.assertEqual(actual, expected)

    def test_readdir_with_normal_1_or_3_file_glob(self):
        actual = list(readdir(test_tree["root dir"], glob="normal-[13]-file"))
        actual.sort()
        expected = list(entry for entry in test_tree["contents: normal-?-file"]
                        if entry.name != "normal-2-file")
        expected.sort()
        self.assertEqual(actual, expected)

    def test_file_has_specified_attributes(self):
        actual = list(readdir(test_tree["root dir"]))
        normal_file = [f
                       for f in actual
                       if f.name == "normal-file"]
        # There should be exactly one of these
        self.assertEqual(len(normal_file), 1)
        normal_file = normal_file[0]
        
        # Make sure all fields exist
        normal_file.name
        normal_file.type
        normal_file.inode

    def test_file_does_not_have_windows_attributes(self):
        actual = list(readdir(test_tree["root dir"]))
        normal_file = [f
                       for f in actual
                       if f.name == "normal-file"]
        # There should be exactly one of these
        self.assertEqual(len(normal_file), 1)
        normal_file = normal_file[0]
        
        # None of these should exist; they are Windows-only
        with self.assertRaises(AttributeError):
            normal_file.attributes

        with self.assertRaises(AttributeError):
            normal_file.creation_time

        with self.assertRaises(AttributeError):
            normal_file.modification_time

        with self.assertRaises(AttributeError):
            normal_file.access_time

        with self.assertRaises(AttributeError):
            normal_file.size

        with self.assertRaises(AttributeError):
            normal_file.short_name



if __name__ == '__main__':
    unittest.main()

