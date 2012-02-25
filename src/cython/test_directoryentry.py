from generic import DirectoryEntry, RegularFile
import unittest

class Tests(unittest.TestCase):
    def setUp(self):
        self.e = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)

    def test_get_name(self):
        self.assertEqual("foo", self.e.name)

    def test_get_path(self):
        self.assertEqual("/bar/baz", self.e.path)

    def test_get_kind(self):
        self.assertIs(RegularFile, self.e.kind)

    def test_get_inode(self):
        self.assertEqual(7, self.e.inode)

    def test_cannot_change_name(self):
        with self.assertRaisesRegexp(TypeError, ".*immutable.*"):
            self.e.name = 7

    def test_cannot_change_inode(self):
        with self.assertRaisesRegexp(TypeError, ".*immutable.*"):
            self.e.inode = 6

    def test_cannot_create_attribute(self):
        with self.assertRaisesRegexp(TypeError, ".*immutable.*"):
            self.e.foobar = 7

    def test_cannot_access_dict(self):
        with self.assertRaisesRegexp(TypeError, ".*immutable.*"):
            d = self.e.__dict__

    def test_exact_dupe(self):
        exact_dupe = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)
        self.assertEqual(self.e, exact_dupe)

    def test_equal_but_different_kind_of_inode_integer(self):
        equal = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertEqual(self.e, equal)

        

if __name__ == '__main__':
    unittest.main()
