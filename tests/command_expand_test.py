import unittest
from components.meng import MutationEngine

class TestImported1(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_asdf(self):
        self.m = MutationEngine()
        self.assertEqual(self.m.mutate("",""), "")