import fileinput
from LAB1.Originals import LA, Regex

STATE_START = "%X"
SIGN_START = "%L"
CLASS_NAME_START = '{'
CLASS_NAME_END = '}'
REGEX_GROUP_START = '('
REGEX_GROUP_END = ')'
COMMAND_START = '{'
COMMAND_END = '}'
NAME_PREFIX = '<'
NAME_SUFFIX = '>'


class Generator:
    def __init__(self, text=""):
        self.regExpressions = list()
        self.states = list()
        self.signs = list()
        self.rules = []

        if text == "":
            self.text = readLines()
        else:
            self.text = text.splitlines()

        self.regExpressions = self.getRegularExpressions(self.text)
        self.states = self.getStates(self.text)
        self.signs = self.getUniformSigns(self.text)

        for c in self.getCommands(self.text, self.regExpressions):
            self.addRule(c)

    # Returns all final named regular expressions in a list.
    def getRegularExpressions(self, text):
        toRet = list()

        for index, line in enumerate(text):
            if line.startswith(STATE_START):
                break

            nameEnd = line.find(CLASS_NAME_END)
            name = line[1:nameEnd]
            chars = line[nameEnd + 2:]
            chars = self.fixRegDef(chars, toRet)

            toRet.append((name, chars))

        return toRet

    # For a regular expression namedRegExs and a database of regular expressions RegExpressions
    # returns the fixed, final regular expression without named regular expressions inside
    def fixRegDef(self, namedRegExs, RegExpressions):
        for re in RegExpressions:
            namedRegExs = namedRegExs.replace(CLASS_NAME_START + re[0] + CLASS_NAME_END,
                                              REGEX_GROUP_START + re[1] + REGEX_GROUP_END)
        return namedRegExs

    # Returns all identified stats in a list
    def getStates(self, text):
        return text[findIndexWhenStarting(text, STATE_START)][3:].split(' ')

    # Returns all identified entities in a list.
    def getUniformSigns(self, text):
        return text[findIndexWhenStarting(text, SIGN_START)][3:].split(' ')

    # Returns a list of all commands in the form of tuples - (Starting state, regular expression, list of commands)
    def getCommands(self, text, regexList):
        toRet = list()
        lines = text[findIndexWhenStarting(text, NAME_PREFIX):]

        while lines:
            nameEndIndex = lines[0].find(NAME_SUFFIX)
            startingState = lines[0][1:nameEndIndex]
            RegExpression = self.fixRegDef(lines[0][nameEndIndex + 1:], regexList)

            commands = list()
            for index, line in enumerate(lines[2:]):
                if line == COMMAND_END:
                    lines = lines[index + 3:]
                    break
                commands.append(line)

            toRet.append((startingState, RegExpression, commands))

        return toRet

    # Adds a rule into rules. Rule set is of format [state, regular expression string, commands].
    def addRule(self, ruleset):
        self.rules.append((ruleset[0], Regex.RegularExpression(ruleset[1]), ruleset[2]))

    def toString(self):
        print("States:", self.states)
        print("Uniform signs:", self.signs)
        print("Rules:")

        for r in self.rules:
            print(r[0] + ", \"" + r[1].expression + "\"", ":\n", r, "\n")

# Reads from stdin and returns the read lines as a list.
def readLines():
    lines = list()
    for line in fileinput.input():
        if line == '\n':
            break
        lines.append(line[:-1])
    return lines

# Returns the index of an element in a string list that starts with startsWith
def findIndexWhenStarting(list, startsWith):
    for i, x in enumerate(list):
        if x[0:len(startsWith)] == startsWith:
            return i

    return -1

def main():
    gen = Generator()
    la = LA.LA(gen)


# main()
