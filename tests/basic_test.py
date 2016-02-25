import unittest
from components.meng import MutationEngine

class TestImported1(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_(self):
        self.m = MutationEngine()
        body = self.m.mutate("a","swap a b")
        self.assertEqual(body, "b")

    def tearDown(self):
        self.m = None