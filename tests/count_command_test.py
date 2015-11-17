import unittest
from ..components.meng import *

m = MutationEngine()

class TestCountCommand(unittest.TestCase):

    def setUp(self):
        self.orig = ''

    def test_null_input(self):
        self.orig = ''
        self.assertEqual(int(m.mutate(self.orig,'count')), 0)
        self.assertEqual(int(m.mutate(self.orig,'count -l')), 1)
        self.assertEqual(int(m.mutate(self.orig,'count -w')), 0)
        self.assertEqual(int(m.mutate(self.orig,'count -s a')), 0)

    def test_single_char(self):
        self.orig = 'a'
        self.assertEqual(int(m.mutate(self.orig,'count')), 1)

    def test_multiple_char(self):
        self.orig = 'a#1'
        self.assertEqual(int(m.mutate(self.orig,'count')), 3)

    def test_whitespace_char(self):
        self.orig = ' '
        self.assertEqual(int(m.mutate(self.orig,'count')), 1)

    def test_newline_char(self):
        self.orig = '\n'
        self.assertEqual(int(m.mutate(self.orig,'count')), 1)

    def test_mixed_whitespace_char(self):
        self.orig = 'a b'
        self.assertEqual(int(m.mutate(self.orig,'count')), 3)

    def test_mixed_newline_char(self):
        self.orig = 'a\nb'
        self.assertEqual(int(m.mutate(self.orig,'count')), 3)

    def test_single_line(self):
        self.orig = '\n'
        self.assertEqual(int(m.mutate(self.orig,'count -l')), 2)

    def test_multiple_line(self):
        self.orig = '\n\n'
        self.assertEqual(int(m.mutate(self.orig,'count -l')), 3)

    def test_single_word(self):
        self.orig = 'foo'
        self.assertEqual(int(m.mutate(self.orig,'count -w')), 1)

    def test_multiple_word(self):
        self.orig = 'foo bar'
        self.assertEqual(int(m.mutate(self.orig,'count -w')), 2)

    def test_char_substr(self):
        self.orig = 'a'
        self.assertEqual(int(m.mutate(self.orig,'count -s a')), 1)

    def test_word_substr(self):
        self.orig = 'foo'
        self.assertEqual(int(m.mutate(self.orig,'count -s foo')), 1)

    def test_multiple_char_substr(self):
        self.orig = 'a aa'
        self.assertEqual(int(m.mutate(self.orig,'count -s a')), 3)

    def test_multiple_word_substr(self):
        self.orig = 'foo foofoo'
        self.assertEqual(int(m.mutate(self.orig,'count -s foo')), 3)

if __name__ == '__main__':
    unittest.main()