import __future__

# Helpers
def simple_expr(expression):
    restrict_chars = (' ','+','-','/','*','^','%')
    back_ops = tuple('(') + restrict_chars
    fwd_ops = tuple(')') + restrict_chars
    x, i = expression, 0
    x = "("+x+")"
    end_size = len(x)
    while (i < len(x)-1):
        if (i > 0):
            if x[i] == '(' and x[i-1] not in back_ops and x[i+1] not in fwd_ops:
                x = x[:i] + '*' + x[i:]
            elif x[i] == ')' and x[i-1] not in back_ops and x[i+1] not in fwd_ops:
                x = x[:i+1] + '*' + x[i+1:]
            elif x[i] == '^':
                x = x[:i] + '**' + x[i+1:]
            end_size += 1
            i += 1
        i += 1
    return eval(compile(x, '<string>', 'eval', __future__.division.compiler_flag))

# Classes
class ConsoleErrorLogger:

    def displayError(self, message):
        print(message)

# Exception Classes
class InvalidTransmutation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)