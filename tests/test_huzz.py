import unittest
import sys
import os

# ensure local src is used
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import huzz as h

class TestHuzzCore(unittest.TestCase):
    def test_registry_count(self):
        db = h.get_huzz_db()
        # default global registry might be empty unless we add to it
        self.assertEqual(len(db), 0, "default global registry should be empty")

    def test_predicates(self):
        # use new lowercase slang naming
        test_hu = h.HuzzEntity(name="test", fine_shi=True, going=False, aura=50)
        self.assertTrue(test_hu.fine_shi)
        self.assertFalse(test_hu.going)
        self.assertEqual(test_hu.aura, 50)

if __name__ == '__main__':
    unittest.main()
