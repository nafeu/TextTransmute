import getopt
import unittest
import ast
import operator as op

class Transmutation(object):

    def __init__(self, error_module=None):
        self.body = None
        self.error_module = error_module
        self.command = self.__class__.__name__.lower()

    def display_error(self, message):
        if self.error_module:
            self.error_module.display_error(message)
        else:
            print(message)

    def transmute(self, body, params=None):
        self.body = body

        # Mutation Case Algorithms
        def default():
            return self.body

        def other_case():
            return self.body + self.body

        # Option Parsing
        try:
            opts, args = getopt.getopt(params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_error("Transmutation Error: " + str(err) + " for " + self.command)
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-l":
                return other_case()

        # Arg Handling
        if args:
            argument = args[0]

        # default
        return default()

class TestTransmutation(unittest.TestCase):

    def setUp(self):
        self.t = Transmutation()

    def test_default(self):
        self.assertEqual(self.t.transmute("asdf"), "asdf")

    def test_other_case(self):
        self.assertEqual(self.t.transmute("asdf", ['-l']), "asdfasdf")

class Rev(Transmutation):

    def transmute(self, body, params=None):
        return body[::-1]

class TestRev(unittest.TestCase):

    def setUp(self):
        self.t = Rev()

    def test_default(self):
        self.assertEqual(self.t.transmute("asdf"), "fdsa")

class Expr(Transmutation):

    def transmute(self, body, params=None):
        return eval_expr(body)

class TestExpr(unittest.TestCase):

    def setUp(self):
        self.t = Expr()

    def test_default(self):
        self.assertEqual(self.t.transmute("2 + 2"), 4)
        self.assertEqual(self.t.transmute("2 * 2"), 4)
        self.assertEqual(self.t.transmute("2 + (2 * 2)"), 6)

# Helpers

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
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
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)