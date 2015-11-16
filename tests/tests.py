import unittest
from ..components.meng import *

class TestCountCommand(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def tearDown(self):
        print('init teardown')

    def test_linecount(self):
        orig = 'a'
        compare = int(self.m.mutate(orig,'count'))
        self.assertEqual(compare, 1)

def runTests():
    unittest.main()

if __name__ == '__main__':
    runTests()