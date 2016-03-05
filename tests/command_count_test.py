import unittest
from components.meng import MutationEngine

class TestCountCommand(unittest.TestCase):

    def setUp(self):
        self.m = MutationEngine()

    def test_default_char_count(self):
        self.assertEqual(int(self.m.mutate('', 'count')), 0)
        self.assertEqual(int(self.m.mutate('a', 'count')), 1)
        self.assertEqual(int(self.m.mutate('a#1', 'count')), 3)
        self.assertEqual(int(self.m.mutate(' ', 'count')), 1)
        self.assertEqual(int(self.m.mutate('\n', 'count')), 1)
        self.assertEqual(int(self.m.mutate('a b', 'count')), 3)
        self.assertEqual(int(self.m.mutate('a\nb', 'count')), 3)

    def test_line_count(self):
        self.assertEqual(int(self.m.mutate('', 'count -l')), 1)
        self.assertEqual(int(self.m.mutate('\n', 'count -l')), 2)
        self.assertEqual(int(self.m.mutate('\n\n', 'count -l')), 3)

    def test_word_count(self):
        self.assertEqual(int(self.m.mutate('', 'count -w')), 0)
        self.assertEqual(int(self.m.mutate('foo', 'count -w')), 1)
        self.assertEqual(int(self.m.mutate('foo bar', 'count -w')), 2)

    def test_string_count(self):
        self.assertEqual(int(self.m.mutate('', 'count -s a')), 0)
        self.assertEqual(int(self.m.mutate('a', 'count -s a')), 1)
        self.assertEqual(int(self.m.mutate('foo', 'count -s foo')), 1)
        self.assertEqual(int(self.m.mutate('a aa', 'count -s a')), 3)
        self.assertEqual(int(self.m.mutate('foo foofoo', 'count -s foo')), 3)