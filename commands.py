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
    """Evaluate simple expressions: '3 + 3' -> 6, '3 * 3' -> 9"""

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