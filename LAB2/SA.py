SIGN_SEPARATOR = "\n"
SIGN_PROPERTY_SEPARATOR = " "

# todo Remove when everything is done.
test_string = """OPERAND 2 3
OP_MINUS 2 -
UMINUS 2 -
OPERAND 2 0x12
OP_MINUS 2 -
LIJEVA_ZAGRADA 2 (
OPERAND 4 3
OP_MINUS 4 -
UMINUS 4 -
UMINUS 5 -
UMINUS 5 -
OPERAND 5 076
DESNA_ZAGRADA 5 )
"""


# Holds sing pairs into a list as tuples (triples)
class UniformSignSeries:

    def __init__(self, source):
        self.content = self.parse(source)

    # Parses the specifically formatted input; puts all sign pairs into self.content.
    @staticmethod
    def parse(source):
        to_ret = list()

        lines = filter(None, source.split(SIGN_SEPARATOR))

        for l in lines:
            temp_l = l.strip()
            l = temp_l.split(SIGN_PROPERTY_SEPARATOR, 2)
            to_ret.append((l[0], l[1], l[2]))

        return to_ret

    # Returns a list of signs appearing causally.
    def get_signs(self):
        return [x[0] for x in self.content]

    def __str__(self):
        to_ret = ""

        for c in self.content:
            to_ret += str(c[0]) + " " + str(c[1]) + " " + str(c[2]) + "\n"

        return to_ret[0:-1]
