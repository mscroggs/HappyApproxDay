from itertools import product
import math
import sympy

constants = [
    (math.pi, u"\u03C0", "pi"),
    (2 * math.pi, u"\u03C4", "tau",),
    (math.sqrt(2), u"\u221A2", "root2"),
    (math.sqrt(3), u"\u221A3", "root3"),
    (math.e, "e", "e"),
    ((1 + math.sqrt(5)) / 2, u"\u03D5", "phi"),
    (9.81, "g", "g"),
]


def str_to_combine(value):
    if isinstance(value, BaseConstant):
        return value.str_to_combine()
    return str(value)


class BaseConstant:
    def __init__(self, value, string, includes):
        assert value > 0
        self.value = value
        self.string = string
        self.includes = includes

    def error(self, value):
        return abs(value - self.value) / self.value

    def __str__(self):
        return str(self.as_sympy()).replace("*", "").replace(" ", "")

    def to_html(self):
        map = {u"\u03C0": "&pi;", u"\u03C4": "&tau;",
               u"\u221A2": "&radic;2", u"\u221A3": "&radic;3"}
        return "".join([map[char] if char in map else char
                        for char in self.string])

    def as_sympy(self):
        raise NotImplementedError()

    def str_to_combine(self):
        return "(" + self.string + ")"


class Constant(BaseConstant):
    def __init__(self, value, string, name):
        super().__init__(value, string, {name})

    def str_to_combine(self):
        return self.string

    def as_sympy(self):
        return sympy.Symbol(self.string)


class Difference(BaseConstant):
    def __init__(self, a, b):
        super().__init__(
            a.value - b.value,
            str_to_combine(a) + "-" + str_to_combine(b),
            a.includes.union(b.includes))
        self.a = a
        self.b = b

    def as_sympy(self):
        return self.a.as_sympy() - self.b.as_sympy()


class Sum(BaseConstant):
    def __init__(self, a, b):
        super().__init__(
            a.value + b.value,
            str_to_combine(a) + "+" + str_to_combine(b),
            a.includes.union(b.includes))
        self.a = a
        self.b = b

    def as_sympy(self):
        return self.a.as_sympy() + self.b.as_sympy()


class Product(BaseConstant):
    def __init__(self, a, b):
        super().__init__(
            a.value * b.value,
            str_to_combine(a) + str_to_combine(b),
            a.includes.union(b.includes))
        self.a = a
        self.b = b

    def as_sympy(self):
        return self.a.as_sympy() * self.b.as_sympy()


class Multiple(BaseConstant):
    def __init__(self, a, b):
        assert isinstance(a, int)
        super().__init__(
            a * b.value,
            str_to_combine(a) + str_to_combine(b),
            b.includes.union({"multiple"}))
        self.a = a
        self.b = b

    def as_sympy(self):
        return self.a * self.b.as_sympy()


class Sin(BaseConstant):
    def __init__(self, a):
        super().__init__(
            math.sin(a.value),
            "sin(" + str_to_combine(a) + ")",
            a.includes.union({"sin"}))
        self.a = a

    def as_sympy(self):
        return sympy.sin(self.a.as_sympy())


class Cos(BaseConstant):
    def __init__(self, a):
        super().__init__(
            math.cos(a.value),
            "cos(" + str_to_combine(a) + ")",
            a.includes.union({"cos"}))
        self.a = a

    def as_sympy(self):
        return sympy.cos(self.a.as_sympy())


class Tan(BaseConstant):
    def __init__(self, a):
        super().__init__(
            math.tan(a.value),
            "tan(" + str_to_combine(a) + ")",
            a.includes.union({"tan"}))
        self.a = a

    def as_sympy(self):
        return sympy.tan(self.a.as_sympy())


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

    for c in options:
        if math.sin(c.value) > 0:
            new.append(Sin(c))
        if math.cos(c.value) > 0:
            new.append(Cos(c))
        if math.tan(c.value) > 0:
            new.append(Tan(c))

    for c, d in product(options, options):
        if len(c.includes.intersection(d.includes)) == 0:
            new.append(Sum(c, d))
            if c.value > d.value:
                new.append(Difference(c, d))
            elif d.value > c.value:
                new.append(Difference(d, c))
            if (
                "+" not in str(c)
                and "-" not in str(c)
                and "multiple" not in c.includes
                and "+" not in str(d)
                and "-" not in str(d)
                and "multiple" not in d.includes
                and not math.isclose(c.value, d.value)
            ):
                new.append(Product(c, d))
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
        difference = c.value - value
        closest_int = int(math.floor(difference + 0.5))
        if abs(difference - closest_int) / value <= 0.002:
            if closest_int == 0:
                out.append(c)
            elif "int" not in c.includes:
                if closest_int > 0:
                    out.append(Difference(
                        c, Constant(closest_int, str(closest_int), "int")))
                else:
                    out.append(Sum(
                        c, Constant(-closest_int, str(-closest_int), "int")))
    return out
