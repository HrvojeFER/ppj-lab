from LAB1.New import Regex
import General

NEW_LINE = '\n'
STATE_START_SIGN = '<'
STATE_END_SIGN = '>'
COMMAND_START_SIGN = '{'
COMMAND_END_SIGN = '}'
STATES_START_SIGN = "%X"
SIGNS_START_SIGN = "%L"
REGEX_DELIMITER = '\n'
STATES_DELIMITER = ' '
SIGNS_DELIMITER = ' '
INDIVIDUAL_REGEX_DELIMITER = ' '
REGEX_NAME_START = '{'
REGEX_NAME_END = '}'
GROUP_START = '('
GROUP_END = ')'


class Generator:
    def __init__(self, text):
        self.regex_dict, self.states, self.signs, self.rules = self.parse_lexer(text)

    # Returns the regular expressions, the states, the unique signs and the rules of a given lexer description.
    @staticmethod
    def parse_lexer(text):

        part1 = text.split(STATES_START_SIGN)                                       # Splits it into Regex and the rest
        part2 = part1[1].split(SIGNS_START_SIGN)                                    # Splits it into states and the rest
        part3 = part2[1].split(NEW_LINE, 1)                                         # Splits it into signs and the rest
        part4 = part3[1].rsplit(COMMAND_END_SIGN + NEW_LINE + STATE_START_SIGN)     # Splits the rules into individual rules

        regex = part1[0].split(REGEX_DELIMITER)
        regex_dict = {}

        for r in regex:
            if not r.startswith(REGEX_NAME_START):
                continue

            part1 = r.split(INDIVIDUAL_REGEX_DELIMITER, 1)
            name = part1[0].replace(REGEX_NAME_START, '')
            name = name.replace(REGEX_NAME_END, '')

            expression = part1[1]

            for rr in regex_dict:
                expression = expression.replace(REGEX_NAME_START + rr + REGEX_NAME_END,
                                                GROUP_START + regex_dict[rr] + GROUP_END)

            regex_dict[name] = expression

        states = part2[0].split(STATES_DELIMITER)
        signs = part3[0].split(SIGNS_DELIMITER)
        rules = set()

        for rule in part4:
            to_ret = rule

            if not rule.startswith(STATE_START_SIGN):
                to_ret = STATE_START_SIGN + to_ret

            if not rule.endswith(COMMAND_END_SIGN):
                to_ret = rule + COMMAND_END_SIGN

            rules.add(Rule(regex_dict, to_ret))

        return regex_dict, states, signs, rules

    @staticmethod
    def normalize_regex(regex):
        regex_dict = {}

        for r in regex:
            if not r.startswith(REGEX_NAME_START):
                continue

            part1 = r.split(INDIVIDUAL_REGEX_DELIMITER, 1)
            name = part1[0].replace(REGEX_NAME_START, '')
            name = name.replace(REGEX_NAME_END, '')

            expression = part1[1]

            for rr in regex_dict:
                expression = expression.replace(REGEX_NAME_START + rr + REGEX_NAME_END, GROUP_START + regex_dict[rr] + GROUP_END)

            regex_dict[name] = expression

        return regex_dict

    @staticmethod
    def fix_regex(regex_dict, regex):
        for r in regex_dict:
            regex = regex.replace(REGEX_NAME_START + r + REGEX_NAME_END, GROUP_START + regex_dict[r] + GROUP_END)

        return regex


class Rule:
    def __init__(self, regex_dict, text):
        self.state, self.regex, self.commands = self.parse_rule(regex_dict, text)

    def __str__(self):
        to_ret = "When in state " + self.state + ", matching " + self.regex.expression + ", do:\n"

        for c in self.commands:
            to_ret += c + '\n'

        return to_ret

    # Parses a single lexer rule and returns the state, the regular expression that triggers the rule, and the set of
    # commands that are executed upon trigger
    @staticmethod
    def parse_rule(regex_dict, text):
        part1 = text.split(NEW_LINE, 1)                 # Splits it into <name>regex and command
        part2 = part1[0].split(STATE_END_SIGN, 1)       # Splits it into <name and regex

        state = part2[0][part2[0].find(STATE_START_SIGN) + 1:]
        regex = Regex.RegularExpression(Generator.fix_regex(regex_dict, part2[1]))
        commands = (part1[1][part1[1].find(COMMAND_START_SIGN) + 2:part1[1].find(COMMAND_END_SIGN)]).split(NEW_LINE)

        return state, regex, commands


def main():
    t = open("../Originals/Tests/simplePpjLang.lan", 'r').read()

    gen = Generator(t)

    for r in gen.rules:
        print(r)


# print("Time needed:", General.benchmark_function_string(main))
