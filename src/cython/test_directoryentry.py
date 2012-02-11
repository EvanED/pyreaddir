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
        with self.assertRaises(TypeError):
            self.e.name = 7

    def test_cannot_change_inode(self):
        with self.assertRaises(TypeError):
            self.e.inode = 6

    def test_cannot_create_attribute(self):
        with self.assertRaises(TypeError):
            self.e.foobar = 7

    def test_cannot_access_dict(self):
        with self.assertRaises(TypeError):
            print self.e.__dict__


        

if __name__ == '__main__':
    unittest.main()
