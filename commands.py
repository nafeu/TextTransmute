import getopt
import unittest
import ast
import operator as op
import textwrap

class Transmutation(object):
    """Transmutation example and help"""

    def __init__(self, error_module=None):
        self.body = None
        self.error_module = error_module
        self.command = self.__class__.__name__.lower()

    def display_err(self, message):
        if self.error_module:
            self.error_module.display_err(message)
        else:
            print(message)

    def transmute(self, body=None, params=None):
        self.body = body

        # Mutation Case Algorithms
        def default():
            desc = ('This plugin allows you to mutate, insert or generate '
                    'selected text using bash-inspired commands.')
            return self.body + "\n\n" + desc

        def usage():
            return self.body + "\n\n" + "Usage: command -o --option 'args'"

        def version():
            return self.body + ("\n\n%s - %s" % ("TextTransmute v1.0.0",
                                                 "github.com/nafeu"))

        # Option Parsing
        try:
            opts, args = getopt.getopt(params,
                                       'hv',
                                       ["help", "version"])
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return self.body

        # Option Handling
        for o, a in opts:
            if o in ("-v", "--version"):
                return version()
            elif o in ("-h", "--help"):
                return usage()

        # Arg Handling
        if args:
            argument = args[0]

        # default
        return default()


class TestTransmutation(unittest.TestCase):
    """Unit test for Transmutation command"""

    def setUp(self):
        self.t = Transmutation()

    def test_default(self):
        desc = ('This plugin allows you to mutate, insert or generate '
                'selected text using bash-inspired commands.')
        self.assertEqual(self.t.transmute(''), "\n\n" + desc)


class Expr(Transmutation):
    """Evaluate simple expressions"""

    def transmute(self, body=None, params=None):
        try:
            return eval_expr(body)
        except Exception:
            pass
        return body


class TestExpr(unittest.TestCase):
    """Unit test for Expr command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Expr()

    def test_default(self):
        self.assertEqual(self.t.transmute("2 + 2"), 4)
        self.assertEqual(self.t.transmute("2 * 2"), 4)
        self.assertEqual(self.t.transmute("2 + (2 * 2)"), 6)


class Swap(Transmutation):
    """Replace matched substrings inside a selection"""

    def transmute(self, body=None, params=None):

        # Mutation Case Algorithms
        def default():
            return body.replace(old_string, new_string)

        # Option Parsing
        try:
            opts, args = getopt.getopt(params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return body

        # Arg Handling
        if len(args) > 1:
            old_string = args[0]
            new_string = args[1]
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "requires arguments",
                                              "[old string] [new string]"))

        return default()


class TestSwap(unittest.TestCase):
    """Unit test for Swap command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Swap()

    def test_default(self):
        self.assertEqual(self.t.transmute("a", ["a", "x"]), "x")
        self.assertEqual(self.t.transmute("abc", ["b", "d"]), "adc")

class Mklist(Transmutation):
    """Generate alphabetized or numeric lists"""

    def transmute(self, body=None, params=None):

        self.body = body
        self.params = params

        # Helpers
        def place(s, placement):
            return str(placement.replace('{$}', str(s)))

        # Option status
        placement = '{$}'
        range_start = 0
        range_end = 0
        range_increment = 1
        seperator = '\n'
        alphabet = False

        # Mutation Case Algorithms
        def default():
            if alphabet:
                return seperator.join(place(chr(i), placement)
                       for i in range(range_start, range_end, range_increment))
            return seperator.join(place(i, placement)
                   for i in range(range_start, range_end, range_increment))

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params,
                                       'cp:',
                                       ["close", "place="])
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return self.body

        # Option Handling
        for o, a in opts:
            if o in ("-c", "--close"):
                seperator = ''
            elif o in ("-p", "--place"):
                placement = a
                if placement.find('{$}') == -1:
                    placement = a + '{$}'

        # Arg Handling
        if len(args) >= 2:
            try:
                range_start = int(args[0])
                range_end = int(args[1]) + 1
            except ValueError:
                range_start = ord(args[0])
                range_end = ord(args[1]) + 1
                alphabet = True
            try:
                range_increment = int(args[2])
            except IndexError:
                pass
            if range_start > range_end:
                range_increment *= -1
                range_end -= 2
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "requires arguments",
                                              "[start] [end]"))

        # default
        return default()


class TestMklist(unittest.TestCase):
    """Unit test for Mklist command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Mklist()

    def test_default(self):
        self.assertEqual(self.t.transmute("", ["1", "5"]), "1\n2\n3\n4\n5")
        self.assertEqual(self.t.transmute("", ["a", "d"]), "a\nb\nc\nd")
        self.assertEqual(self.t.transmute("", ["-c", "1", "5"]), "12345")
        self.assertEqual(self.t.transmute("", ["-p", "{$}.", "1", "3"]),
                                          "1.\n2.\n3.")


class Dupl(Transmutation):
    """Duplicate selection n times"""

    def transmute(self, body=None, params=None):

        # Option status
        newline = '\n'
        multiplier = 2

        # Mutation Case Algorithms
        def default():
            return ((body + newline) * int(multiplier))

        # Option Parsing
        try:
            opts, args = getopt.getopt(params,
                                       'c',
                                       ["close"])
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return self.body

        # Option Handling
        for o, a in opts:
            if o in ("-c", "--close"):
                newline = ''

        # Arg Handling
        if args:
            multiplier = args[0]

        # default
        return default()


class TestDupl(unittest.TestCase):
    """Unit test for Dupl command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Dupl()

    def test_default(self):
        self.assertEqual(self.t.transmute("a"), "a\na\n")
        self.assertEqual(self.t.transmute("a", ["-c"]), "aa")


class Strip(Transmutation):
    """Strip a matched pattern out of selection"""

    def transmute(self, body=None, params=None):

        pattern = ''

        try:
            opts, args = getopt.getopt(params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return body

        # Arg Handling
        if args:
            pattern = args[0]

        # Mutation Case Algorithms
        def default():
            output = ''
            for line in body.split("\n"):
                output += (line.replace(pattern, "") + "\n")
            return output.rstrip("\n")


        # default
        return default()


class TestStrip(unittest.TestCase):
    """Unit test for Dupl command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Strip()

    def test_default(self):
        self.assertEqual(self.t.transmute("abc", ["b"]), "ac")


class Expand(Transmutation):
    """Expand newline whitespace between lines"""

    def transmute(self, body=None, params=None):

        multiplier = 1

        try:
            opts, args = getopt.getopt(params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_err("%s: %s for %s" % ("Transmutation Error:",
                                                str(err),
                                                self.command))
            return body

        # Arg Handling
        if args:
            multiplier = int(args[0])

        # Mutation Case Algorithms
        def default():
            output = ''
            for i in body.split("\n"):
                output += (i+"\n" + (multiplier * "\n"))
            return output.rstrip("\n")

        # default
        return default()


class TestExpand(unittest.TestCase):
    """Unit test for Expand command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Expand()

    def test_default(self):
        self.assertEqual(self.t.transmute("a\na"), "a\n\na")
        self.assertEqual(self.t.transmute("a\na", ["2"]), "a\n\n\na")


class Compress(Transmutation):
    """Remove whitespace lines between lines"""

    def transmute(self, body=None, params=None):

        # Mutation Case Algorithms
        def default():
            output = ''
            for line in body.split("\n"):
                output += (line.rstrip()+" ")
            return output.rstrip()

        # default
        return default()


class TestCompress(unittest.TestCase):
    """Unit test for Compress command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Compress()

    def test_default(self):
        self.assertEqual(self.t.transmute("a\na"), "a a")


# Helpers

OPERATORS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return OPERATORS[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return OPERATORS[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)