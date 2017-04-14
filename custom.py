import unittest

# Import Transmutation for Sublime Plugin
try:
    from commands import Transmutation
except ImportError:
    pass

# Import Transmutation for Test Runner
try:
    from .commands import Transmutation
except ValueError:
    pass

# Custom Commands (START HERE)

class Custom(Transmutation):

    def transmute(self, body=None, params=None):
        return "Hello World!"

class TestCustom(unittest.TestCase):

    def setUp(self):
        self.t = Custom()

    def test_default(self):
        self.assertEqual(self.t.transmute(), "Hello World!")