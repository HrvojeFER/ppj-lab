class HashableSet:
    def __init__(self, values=None):
        if values is None:
            self.elements = set()
        else:
            self.elements = set(values)

    def add(self, value):
        self.elements.add(value)

    def update(self, values):
        self.elements.update(values)

    def __iter__(self):
        return self.elements.__iter__()

    def __contains__(self, item):
        return item in self.elements

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return len(self.elements.difference(other.elements)) == 0

    def __hash__(self):
        t_elements = sorted(list(self.elements))
        hash_value = 0

        for element in t_elements:
            hash_value ^= hash(element)

        return hash_value

    def __str__(self):
        to_return = "{"

        for element in self.elements:
            to_return += str(element) + ", "

        if len(to_return) > 1:
            to_return = to_return[:-2]

        return to_return + "}"
