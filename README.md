# TextTransmute

An experimental [Sublime Text](https://www.sublimetext.com/) plugin that allows you to mutate selected text in a style inspired by VIM, Emacs macros and unix shell programming tools.

[![Build Status](https://travis-ci.org/nafeu/TextTransmute.svg?branch=master)](https://travis-ci.org/nafeu/TextTransmute)

### How It Works

1. Select some text
2. Select the transmutation(s) you want to perform
3. Watch the text magically change
4. Realize some transmutations don't even need inputs at all
5. Channel your inner alchemist

### Features

- Use a collection of customizable sublime commands to mutate and contextually modify text
- Piping using the `|` character is supported and inspired by stdin/stdout mechanics of a unix shell
- Use knowledge of python to quickly write a command that helps simplify repetitive coding tasks
- Create aliases that run a common/useful sequence of piped commands

#### Requirements

Sublime Text 3

#### Installation

Clone this repository into your Sublime Text `Packages` folder under the directory name `TextTransmute`

```
cd Sublime\ Text\ 3/Packages
git clone https://github.com/nafeu/TextTransmute.git TextTransmute
```

### Usage

Default Key Bindings:

| Command                   | OSX                | Linux/Windows |
|---------------------------|--------------------|---------------|
| **Perform Transmutation** | `ctrl + shift + j` | `ctrl + k, j` |
| **Use Alias**             | `ctrl + shift + h` | `ctrl + k, h` |

All available Sublime Commands:

```
Perform Transmutation
Use Alias
History
Edit/Add Aliases
Edit Key Bindings
Edit/Add Custom Commands
```

### Currently Available Transmutation Commands (more to come)

_`[]` - Mandatory, `()` - Optional_

| Name / Synopsis | Description |
| --------------- | ----------- |
| `http [method] (url) (key) (val) ...` | Perform HTTP GET/POST request using [Requests](http://docs.python-requests.org/en/master/) library |
| `swap [old string] [new string]`  | Swap matched strings with a new string |
| `expr` | Evaluate simple expressions |
| `mklist [#/a-z] [#/a-z] (--close) (--place=[string including {$}])` | Generate alphabetized or numeric lists |
| `dupl (n) (--close)` | Duplicate selection n times |
| `strip [string]` | Strip a matched string out of a selection |
| `expand (n)` | Add an empty whitespace between lines n times |
| `compress` | Compress multiple lines into one line |
| `filter [string]` | Filter for lines that contain a specific string |
| `map (file extension)` | Convert whitespace seperated words into language specific map (hashmap, dict, json, etc) |

### Creating Custom Transmutation Commands

Lets say we want to make a command called `Foo`

0. Open command palette (`cmd + shift + p` on OSX, `ctrl + shift + p` on Linux/Windows) and run `TextTransmute: Edit/Add Custom Commands`

1. Create a new class inheriting from `Transmutation` like so:

```python
class Foo(Transmutation):
    """Convert selected text to 'bar'"""
    ...
```

2. `Foo` or `foo` is how your command will be invoked, it must
    be **ONE WORD** for the plugin to add it to the command library

3. Add the `transmute(self, body=None, params=None)` method to your class like so:

```python
class Foo(Transmutation):
    """Convert selected text to 'bar'"""

    def transmute(self, body=None, params=None, meta=None):
        ...
```

The `transmute` method will be called on the `body` of text
you have selected. To learn about the `params` argument,
observe the base `Transmutation` class found inside
[`Packages/TextTransmute/commands.py`](https://github.com/nafeu/TextTransmute/blob/master/commands.py)

4. Return a string in your transmute method, this is what you'll be
   mutating your selected text into

```python
class Foo(Transmutation):
    """Convert selected text to 'bar'"""

    def transmute(self, body=None, params=None, meta=None):
        return "bar"
```

5. Define a test for your command (definitely a more comprehensive one than the following example)

```python
class TestFoo(unittest.TestCase):
    """Unit test for Foo command"""

    def setUp(self):
        self.t = Foo()

    def test_default(self):
        self.assertEqual(self.t.transmute(), "bar")
        self.assertEqual(self.t.transmute("Foo"), "bar")
```

6. Run tests using `python runtests.py`

### Editing Aliases

0. Open command palette (`cmd + shift + p` on OSX, `ctrl + shift + p` on Linux/Windows) and run `TextTransmute: Edit/Add Aliases`

1. Insert or update an alias in the specified format with `Description` and `Command sequence`

```python
ALIASES = [

  ["Generate a list from 1 to 10", "gen -s {$}. 1 10"],
  ["Evaluate this expression", "expr"],
  # ["Description", "Command sequence"],

]
```

### Running the tests

If system is running `Python 3` use:

```python runtests.py```

Otherwise use:

```python3 runtests.py```

#### Development

OSX/Linux:

```
cd Sublime\ Text\ 3/Packages\TextTransmute
pip3 install -r requirements.txt
```

TODO: Add Windows dev instructions...

### License

MIT
