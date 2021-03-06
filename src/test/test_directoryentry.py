from readdir import DirectoryEntry, RegularFile, Directory
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

    def test_exact_dupe_is_equal(self):
        exact_dupe = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)
        self.assertEqual(self.e, exact_dupe)

    def test_equal_but_different_kind_of_inode_integer(self):
        equal = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertEqual(self.e, equal)

    def test_exact_dupe_has_same_hash(self):
        exact_dupe = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7L)
        self.assertEqual(hash(self.e), hash(exact_dupe))

    def test_almost_exact_dupe_has_same_hash(self):
        exact_dupe = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=7)
        self.assertEqual(hash(self.e), hash(exact_dupe))

    def test_different_name_is_unequal(self):
        other = DirectoryEntry("sporz", "/bar/baz", RegularFile, inode=7L)
        self.assertNotEqual(self.e, other)

    def test_different_dir_is_unequal(self):
        other = DirectoryEntry("foo", "/bar/sporz", RegularFile, inode=7L)
        self.assertNotEqual(self.e, other)

    def test_different_type_is_unequal(self):
        other = DirectoryEntry("foo", "/bar/baz", Directory, inode=7L)
        self.assertNotEqual(self.e, other)

    def test_different_inode_is_unequal(self):
        other = DirectoryEntry("foo", "/bar/baz", RegularFile, inode=8L)
        self.assertNotEqual(self.e, other)

    def test_no_inode_is_unequal(self):
        other = DirectoryEntry("foo", "/bar/baz", RegularFile)
        self.assertNotEqual(self.e, other)

    def test_different_name_has_unequal_hash(self):
        other = DirectoryEntry("sporz", "/bar/baz", RegularFile, inode=7L)
        self.assertNotEqual(hash(self.e), hash(other))

    def test_less_than(self):
        a = DirectoryEntry("a", "/b/baz", RegularFile, inode=7)
        dot = DirectoryEntry(".", "/bar/baz", RegularFile, inode=7L)
        self.assertLess(dot, a)
        self.assertGreater(a, dot)
        self.assertLessEqual(a, a)
        self.assertGreaterEqual(a, a)






        

if __name__ == '__main__':
    unittest.main()
