import unittest
from components.meng import MutationEngine

class TestImported1(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_character(self):
        self.assertEqual(self.m.mutate("a", "dupl"), "a\na")
        self.assertEqual(self.m.mutate(" ", "dupl"), " \n ")
        self.assertEqual(self.m.mutate("", "dupl"), "aaaasdfsdfasdfasdfas")