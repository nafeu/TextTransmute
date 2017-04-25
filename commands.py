import getopt
import unittest
import ast
import operator as op
import textwrap
import re
import requests
import markdown
from bs4 import BeautifulSoup

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

    def transmute(self, body=None, params=None, meta=None):
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

    def transmute(self, body=None, params=None, meta=None):
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

    def transmute(self, body=None, params=None, meta=None):

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

    def transmute(self, body=None, params=None, meta=None):

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

    def transmute(self, body=None, params=None, meta=None):

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

    def transmute(self, body=None, params=None, meta=None):

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

    def transmute(self, body=None, params=None, meta=None):

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

    def transmute(self, body=None, params=None, meta=None):

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


class Filter(Transmutation):
    """Filter for lines that contain a specific string"""

    def transmute(self, body=None, params=None, meta=None):

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
        if len(args) > 0:
            pattern = args[0]
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "requires arguments",
                                              "[pattern]"))

        # Mutation Case Algorithms
        def default():
            output = ''
            for line in body.split("\n"):
                if pattern in line:
                    output += (line + "\n")
            return output.rstrip("\n")

        # default
        return default()


class TestFilter(unittest.TestCase):
    """Unit test for Filter command"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Filter()

    def test_default(self):
        self.assertEqual(self.t.transmute("abc\ndef\nc\n", ["de"]), "def")


class Map(Transmutation):
    """Generate a language specific map"""

    def transmute(self, body=None, params=None, meta=None):

        ws_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        extension = ""

        # Mutation Case Algorithms
        def format_py(indent):
            split_body = [x for x in ws_pattern.split(body)[1::2]]
            leading_ws = " " * (len(body) - len(body.lstrip(' ')))
            output = leading_ws + split_body[0] + " = {\n";
            for i in range(1,len(split_body)):
                if (i % 2 != 0):
                    output += (leading_ws +
                               indent +
                               "\"" +
                               split_body[i].replace("\"", "\\\"") +
                               "\": ")
                else:
                    output += split_body[i] + "\n"
            if (len(split_body) % 2 == 0):
                output += "\"\"\n"
            output += leading_ws + "}"
            return output

        def format_js(indent):
            return "var " + format_py(indent)


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
        if len(args) > 0:
            extension = args[0]
        elif "file_extension" in meta:
            extension = meta["file_extension"]
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "no extension specified",
                                              "[extension]"))
            return body

        if extension == "py":
            return format_py("    ")
        elif extension == "js":
            return format_js("  ")
        elif extension == "clj":
            return format_clj()
        elif extension == "cljs":
            return format_clj()
        else:
            self.display_err("%s: '%s' %s" % ("extension",
                                              extension,
                                              "is not supported"))
            return body


class TestMap(unittest.TestCase):
    """Unit test for Map class"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Map()

    def test_py(self):
        self.assertEqual(self.t.transmute("a b \"c\"", ["py"]),
                         "a = {\n    \"b\": \"c\"\n}")
        self.assertEqual(self.t.transmute("  a b \"c\"", ["py"]),
                         "  a = {\n      \"b\": \"c\"\n  }")
        self.assertEqual(self.t.transmute("a b 1", ["py"]),
                         "a = {\n    \"b\": 1\n}")
        self.assertEqual(self.t.transmute("a b 1", ["py"]),
                         "a = {\n    \"b\": 1\n}")
        self.assertEqual(self.t.transmute("a b", ["py"]),
                         "a = {\n    \"b\": \"\"\n}")

    def test_js(self):
        self.assertEqual(self.t.transmute("a b \"c\"", ["js"]),
                         "var a = {\n  \"b\": \"c\"\n}")


class Http(Transmutation):
    """Execute an http request with requests library"""

    def transmute(self, body=None, params=None, meta=None):

        self.body = body
        ws_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        payload = {}

        # Helpers
        def strip_quotes(input_string):
            if ((input_string[0] == input_string[len(input_string)-1])
                and (input_string[0] in ('"', "'"))):
                return input_string[1:-1]
            return input_string

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
        if len(args) > 0:
            method = args[0]
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "requires http verb",
                                              "[method]"))

        if len(args) > 2:
            url = args[1];
            for i in range(2,len(args)):
                if (i % 2 == 0) and (i < len(args) - 1):
                    payload[args[i]] = args[i + 1]
        else:
            self.body = self.body.replace("\n", " ")
            split_body = [strip_quotes(x) for x in ws_pattern.split(self.body)[1::2]]
            url = split_body[0];
            for i in range(1,len(split_body)):
                if (i % 2 != 0) and (i < len(split_body) - 1):
                    payload[split_body[i]] = split_body[i + 1]

        # Mutation Case Algorithms
        def get():
            r = requests.get(url, params=payload)
            return r.text

        def post():
            r = requests.post(url, params=payload)
            return r.text

            return body

        if method.lower() == "get":
            return get()
        elif method.lower() == "post":
            return post()
        else:
            self.display_err("'%s' %s: %s" % (self.command,
                                              "unsupported method",
                                              method))
            return body


class Markdown(Transmutation):
    """Parse markdown into html"""

    def transmute(self, body=None, params=None, meta=None):

        r = re.compile(r'^(\s*)', re.MULTILINE)
        indentation = r'\1\1'

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
        if args:
            indent_amt = args[0]
            if indent_amt.isdigit():
                indentation = r'\1' * int(indent_amt)
            else:
                self.display_err("'%s' %s: %s" % (self.command,
                                                  "indent must be number",
                                                  "[indentation]"))

        def default():
            soup = BeautifulSoup(markdown.markdown(body), 'html.parser')
            output = r.sub(indentation, soup.prettify())
            return output

        return default()

class TestMarkdown(unittest.TestCase):
    """Unit test for Markdown class"""

    # TODO: Improve tests...
    def setUp(self):
        self.t = Markdown()

    def test_default(self):
        self.assertEqual(self.t.transmute("# Hello World"),
                         "<h1>\n  Hello World\n</h1>")
        self.assertEqual(self.t.transmute("# Hello World", ["4"]),
                         "<h1>\n    Hello World\n</h1>")


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