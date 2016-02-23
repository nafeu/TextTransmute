import unittest
from ..components.meng import *

# class TestPluginMain(unittest.TestCase):

#     def setUp(self):
#         self.m = MutationEngine()

#     def test_linecount(self):
#         orig = 'a'
#         compare = int(self.m.mutate(orig,'count'))
#         self.assertEqual(compare, 1)

#     def tearDown(self):
#         self.m = None

class TestParseCommand(unittest.TestCase):

    def setUp(self):
        self.pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        command_list = [x.strip() for x in self.pipe_pattern.split(to_parse)[1::2]]

    def test_linecount(self):
        orig = 'a'
        compare = int(self.m.mutate(orig,'count'))
        self.assertEqual(compare, 1)

    def tearDown(self):
        self.m = None

class TestTransmuteCommand(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_linecount(self):
        orig = 'a'
        compare = int(self.m.mutate(orig,'count'))
        self.assertEqual(compare, 1)

    def tearDown(self):
        self.m = None

if __name__ == '__main__':
    unittest.main()