from itertools import product
import math

constants = [
    (math.pi, u"\u03C0", "pi"),
    (2 * math.pi, u"\u03C4", "tau"),
    (math.sqrt(2), u"\u221A2", "root2"),
    (math.sqrt(3), u"\u221A3", "root3")
]


class BaseConstant:
    def __init__(self, value, string, includes):
        assert value > 0
        self.value = value
        self.string = string
        self.includes = includes

    def error(self, value):
        return abs(value - self.value) / self.value

    def __str__(self):
        return self.string


class Constant(BaseConstant):
    def __init__(self, value, string, name):
        super().__init__(value, string, {name})


class Difference(BaseConstant):
    def __init__(self, a, b):
        super().__init__(
            a.value - b.value,
            f"{a}-{b}",
            a.includes.union(b.includes))


class Sum(BaseConstant):
    def __init__(self, a, b):
        super().__init__(
            a.value + b.value,
            f"{a}+{b}",
            a.includes.union(b.includes))


class Multiple(BaseConstant):
    def __init__(self, a, b):
        assert isinstance(a, int)
        super().__init__(
            a * b.value,
            f"{a}{b}",
            b.includes.union({"multiple"}))


def all_constants(combos):
    options = [Constant(*i) for i in constants]

    for i in range(combos):
        options += combine(options)
    return options


def combine(options):
    new = []
    for i in range(2, 6):
        for c in options:
            if "multiple" not in c.includes:
                new.append(Multiple(i, c))

    for c, d in product(options, options):
        if len(c.includes.intersection(d.includes)) == 0:
            new.append(Sum(c, d))
            if c.value > d.value:
                new.append(Difference(c, d))
            elif d.value > c.value:
                new.append(Difference(d, c))

    out = []
    for n in new:
        for c in options:
            if math.isclose(c.value, n.value):
                break
        else:
            out.append(n)
    return out


def get_constants(value, combos):
    """Return constants that are close to value."""
    out = []
    for c in all_constants(combos):
        if abs(c.value % 1 - value % 1) <= 0.1:
            d = int((c.value - value) // 1)
            if d == 0:
                out.append(c)
            elif "int" not in c.includes:
                if d > 0:
                    out.append(Difference(c, Constant(d, str(d), "int")))
                else:
                    out.append(Sum(c, Constant(-d, str(-d), "int")))
    return out
