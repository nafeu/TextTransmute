import unittest
loader = unittest.TestLoader()
tests = loader.discover('commands', pattern = '*.py')
unittest.TextTestRunner(verbosity=2).run(tests)