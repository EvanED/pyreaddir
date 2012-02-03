from generic import (DirectoryEntry, RegularFile, Directory,
                     SymbolicLink, NamedPipe)
import unittest

class TestDirectoryEntry(unittest.TestCase):
    def test_equal_dirents(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertEquals(first, second)
        self.assertEquals(second, first)

    def test_equal_inodes_one_long(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)
        second = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertEquals(first, second)
        self.assertEquals(second, first)

    def test_disequal_inodes_different_filename(self):
        first = DirectoryEntry("foorzum", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertNotEqual(first, second)
        self.assertNotEqual(second, first)

    def test_disequal_inodes_different_path(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/spork", RegularFile, inode=7)
        self.assertNotEqual(first, second)
        self.assertNotEqual(second, first)

    def test_disequal_inodes_different_type(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/baz", Directory, inode=7)
        self.assertNotEqual(first, second)
        self.assertNotEqual(second, first)

    def test_disequal_inodes_no_attrs(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/baz", RegularFile)
        self.assertNotEqual(first, second)
        self.assertNotEqual(second, first)

    def test_disequal_inodes_different_attrs(self):
        first = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        second = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=8)
        self.assertNotEqual(first, second)
        self.assertNotEqual(second, first)

if __name__ == '__main__':
    unittest.main()

