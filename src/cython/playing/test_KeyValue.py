from KeyValue import KeyValue
import unittest

class TestKeyValue(unittest.TestCase):
    def test_construction_nothrow(self):
        p = KeyValue(0,0)

    def test_exact_same_equal(self):
        p1 = KeyValue(0, 0)
        p2 = KeyValue(0, 0)
        self.assertEqual(p1, p2)

    def test_same_key_different_value_equal(self):
        p1 = KeyValue(0, 0)
        p2 = KeyValue(0, 1)
        self.assertEqual(p1, p2)

    def test_different_keys_unequal(self):
        p1 = KeyValue(0, 0)
        p2 = KeyValue(1, 0)
        self.assertNotEqual(p1, p2)

    def test_lt_depends_on_key(self):
        p1 = KeyValue(0, 1)
        p2 = KeyValue(1, 0)
        self.assertLess(p1, p2)
        self.assertGreater(p2, p1)

        p1 = KeyValue(0, 0)
        p2 = KeyValue(1, 1)
        self.assertLess(p1, p2)
        self.assertGreater(p2, p1)

    def test_lt_false_for_equals(self):
        p1 = KeyValue(0,0)
        p2 = KeyValue(0,0)
        self.assertFalse(p1 < p2)

    def test_key_gets_key(self):
        p1 = KeyValue(1, 2)
        self.assertEquals(1, p1.key())

    def test_value_gets_value(self):
        p1 = KeyValue(1, 2)
        self.assertEquals(2, p1.value())


if __name__ == '__main__':
    unittest.main()
