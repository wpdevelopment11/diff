"""Classes that represent the diff commands."""

class Hunk:
    operation = None

    def op_str(self, arange, brange):
        def get_lines(range):
            if isinstance(range, tuple) and range[0] != range[1]:
                return f"{range[0]},{range[1]}"
            elif isinstance(range, tuple):
                return str(range[0])
            else:
                return str(range)
        return get_lines(arange) + self.operation + get_lines(brange)

    def create_range(self, seq, range, prefix):
        start = range[0] - 1
        end = range[1]
        return [f"{prefix} {el}" for el in seq[start:end]]

    def __repr__(self):
        return str(vars(self))

class Add(Hunk):
    operation = "a"

    def __init__(self, apos, b, brange):
        self.apos = apos
        self.b = b
        self.brange = brange

    def __str__(self):
        hunk = [self.op_str(self.apos, self.brange)]
        hunk += self.create_range(self.b, self.brange, ">")
        return "\n".join(hunk)

    def __eq__(self, other):
        if not isinstance(other, Add):
            return NotImplemented
        return vars(self) == vars(other)

    def invert(self):
        return Delete(self.b, self.brange, self.apos)

class Delete(Hunk):
    operation = "d"

    def __init__(self, a, arange, bpos):
        self.a = a
        self.arange = arange
        self.bpos = bpos

    def __str__(self):
        hunk = [self.op_str(self.arange, self.bpos)]
        hunk += self.create_range(self.a, self.arange, "<")
        return "\n".join(hunk)

    def __eq__(self, other):
        if not isinstance(other, Delete):
            return NotImplemented
        return vars(self) == vars(other)

    def invert(self):
        return Add(self.bpos, self.a, self.arange)

class Replace(Hunk):
    operation = "c"

    def __init__(self, a, arange, b, brange):
        self.a = a
        self.arange = arange
        self.b = b
        self.brange = brange

    def __str__(self):
        hunk = [self.op_str(self.arange, self.brange)]
        hunk += self.create_range(self.a, self.arange, "<")
        hunk += ["---"]
        hunk += self.create_range(self.b, self.brange, ">")
        return "\n".join(hunk)

    def __eq__(self, other):
        if not isinstance(other, Replace):
            return NotImplemented
        return vars(self) == vars(other)

    def invert(self):
        return Replace(self.b, self.brange, self.a, self.arange)
