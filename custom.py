import unittest

# Import Transmutation for Sublime Plugin
try:
    from commands import Transmutation
except ImportError:
    pass

# Import Transmutation for test runner
try:
    from .commands import Transmutation
except (ValueError, SystemError):
    pass

'''
   ___  _   _  ___  _____  ___   __  __
  / __|| | | |/ __||_   _|/ _ \ |  \/  |
 | (__ | |_| |\__ \  | | | (_) || |\/| |
  \___| \___/ |___/  |_|  \___/ |_|  |_|
   ___  ___   __  __  __  __    _    _  _  ___   ___
  / __|/ _ \ |  \/  ||  \/  |  /_\  | \| ||   \ / __|
 | (__| (_) || |\/| || |\/| | / _ \ | .` || |) |\__ \
  \___|\___/ |_|  |_||_|  |_|/_/ \_\|_|\_||___/ |___/

  ----------------------------------------------------
  // TUTORIAL - START HERE!
  ----------------------------------------------------

  0. Lets say we want to make a command called 'Foo' which will swap
     any selection you have with the string "bar"

  1. Create a new class inheriting from Transmutation like so:

    class Foo(Transmutation):
        ...

  2. 'Foo' or 'foo' is how your command will be invoked, it must
      be ONE WORD for the plugin to add it to the command library

  3. Add the 'transmute' method to your class like so

    class Foo(Transmutation):

        def transmute(self, body=None, params=None):
            ...

    The 'transmute' method will be called on the 'body' of text
    you have selected. To learn about the 'params' argument,
    observe the base 'Transmutation' class found inside
    'Packages/TextTransmute/commands.py'

  4. Return a string in your transmute method, this is what you'll be
     mutating your selected text into

'''

class Foo(Transmutation):
    """Foo desc"""
    def transmute(self, body=None, params=None):
        return "bar"

#  5. Define a test for your command

class TestFoo(unittest.TestCase):

    def setUp(self):
        self.t = Foo()

    def test_default(self):
        self.assertEqual(self.t.transmute(), "bar")
        self.assertEqual(self.t.transmute("Foo"), "bar")
        self.assertEqual(self.t.transmute("foo"), "bar")

#  6. Run the test using 'python Packages/TextTransmute/runtests.py'

#  7. Check out the following example commands

class Rev(Transmutation):
    """Rev desc"""
    def transmute(self, body=None, params=None):
        return body[::-1]

class TestRev(unittest.TestCase):

    def setUp(self):
        self.t = Rev()

    def test_default(self):
        self.assertEqual(self.t.transmute("a"), "a")
        self.assertEqual(self.t.transmute("ab"), "ba")
        self.assertEqual(self.t.transmute("abc"), "cba")

class Leet(Transmutation):
    """Leet desc"""
    def transmute(self, body=None, params=None):
        return (body.lower()
                .replace("e", "3").replace("E", "3")
                .replace("l", "1").replace("L", "1")
                .replace("t", "7").replace("T", "7")
                .replace("o", "0").replace("O", "0")
                .replace("s", "5").replace("S", "5"))

class TestLeet(unittest.TestCase):

    def setUp(self):
        self.t = Leet()

    def test_default(self):
        self.assertEqual(self.t.transmute("Leet Noobs"), "1337 n00b5")


'''
Please feel free to contribute your best custom commands to the plugin!
github.com/nafeu/TextTransmute

Add your custom commands below...
'''