
# Text Transmute

An experimental [Sublime Text](https://www.sublimetext.com/) plugin that allows you to mutate selected text in a style inspired by VIM, Emacs and unix shell programming tools.

[![Build Status](https://travis-ci.org/nafeu/TextTransmute.svg?branch=master)](https://travis-ci.org/nafeu/TextTransmute)

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

### Creating Custom Commands

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

3. Add the 'transmute' method to your class like so:

```python
class Foo(Transmutation):
    """Convert selected text to 'bar'"""

    def transmute(self, body=None, params=None):
        ...
```

The `transmute` method will be called on the `body` of text
you have selected. To learn about the `params` argument,
observe the base `Transmutation` class found inside
`Packages/TextTransmute/commands.py`

4. Return a string in your transmute method, this is what you'll be
   mutating your selected text into

```python
class Foo(Transmutation):
    """Convert selected text to 'bar'"""

    def transmute(self, body=None, params=None):
        """Convert selected text to 'bar'"""
        return "bar"
```

5. Define a test for your command

```python
class TestFoo(unittest.TestCase):
    """Unit test for Foo command"""

    def setUp(self):
        self.t = Foo()

    def test_default(self):
        self.assertEqual(self.t.transmute(), "bar")
        self.assertEqual(self.t.transmute("Foo"), "bar")
```

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

```
python runtests.py
```

### License

MIT
