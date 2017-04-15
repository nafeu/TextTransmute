# Text Transmute

An experimental [Sublime Text](https://www.sublimetext.com/) plugin that allows you to mutate selected text in a style inspired by VIM, Emacs and unix shell programming tools.

### Requirements

Sublime Text 3

### Installation

Clone this repository into your Sublime Text `Packages` folder

### Usage

TODO: add default keybindings and keybinding edit information and usage gif

### Tutorial: Creating Custom Commands

Lets say we want to make a command called `Foo`

0. Open the `custom.py` file to edit (located in  `Packages/TextTransmute`)

1. Create a new class inheriting from `Transmutation` like so:

```python
class Foo(Transmutation):
    ...
```

2. `Foo` or `foo` is how your command will be invoked, it must
    be **ONE WORD** for the plugin to add it to the command library

3. Add the 'transmute' method to your class like so:

```python
class Foo(Transmutation):

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

    def transmute(self, body=None, params=None):
        return "Bar"
```

5. Define a test for your command

```python
class TestFoo(unittest.TestCase):

    def setUp(self):
        self.t = Foo()

    def test_default(self):
        self.assertEqual(self.t.transmute(), "Bar")
        self.assertEqual(self.t.transmute("Foo"), "Bar")
```

### Running the tests

```
python runtests.py
```

### License

MIT
