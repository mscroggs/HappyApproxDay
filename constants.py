import math


class BaseConstant:
    def __init__(self, value):
        self.value = value

    def error(self, value):
        return abs(value - self.value)


class Constant(BaseConstant):
    def __init__(self, value, string):
        super().__init__(value)
        self.string = string


constants = [
    Constant(math.pi, "pi"),
    Constant(2 * math.pi, "tau")
]


def get_constants(n):
    """Return constants between n and n+1."""
    return [i for i in constants if n <= i.value <= n + 1]
