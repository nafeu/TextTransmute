import unittest
from components.meng import MutationEngine

class TestCommandRev(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_null(self):
        self.assertEqual(self.m.mutate("", "rev"), "")

    def test_single_char(self):
        self.assertEqual(self.m.mutate("a", "rev"), "a")

    def test_multiple_char(self):
        self.assertEqual(self.m.mutate("abc", "rev"), "cba")