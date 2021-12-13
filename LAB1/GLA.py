from __future__ import print_function
import sys
import os

STATE_START = "%X"
SIGN_START = "%L"
REGEX_NAME_START = '{'
REGEX_NAME_END = '}'
REGEX_GROUP_START = '('
REGEX_GROUP_END = ')'
COMMAND_START = '{'
COMMAND_END = '}'
NAME_PREFIX = '<'
NAME_SUFFIX = '>'
LA_FILE_PATH = 'analizator/LA.py'


# Prints to standard error output
def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Reads from standard input and returns the read lines as a list.
def read_lines():
    lines = list()

    for line in sys.stdin:
        if line == '\n':
            break
        lines.append(line[:-1])

    return lines


# Returns the index of an element in a string list that starts with startsWith
def find_index_starting_with(lines, starts_with):
    for index, line in enumerate(lines):
        if line.startswith(starts_with):
            return index

    return -1


# Contains the regular expression name and the expression itself.
class RegexString:
    def __init__(self, name, regex_string):
        self.name = name
        self.regex_string = regex_string


# Contains the starting state, string and commands for a rule.
class Rule:
    def __init__(self, starting_state, regex_string, commands):
        self.starting_state = starting_state
        self.regex_string = regex_string
        self.commands = commands


class GeneratorData:
    def __init__(self):
        self.regex_string_list = list()
        self.states = list()
        self.signs = list()
        self.rules = list()
        self.starting_state = ''

    def get_data(self):
        text = read_lines()
        self.regex_string_list = self.get_regex_strings(text)
        self.states = self.get_states(text)
        self.starting_state = self.states[0]
        self.signs = self.get_uniform_signs(text)
        self.rules = self.get_rules(text, self.regex_string_list)
        self.print()

    # Returns all final named regular expressions in a list.
    def get_regex_strings(self, text):
        regex_string_list = list()

        for index, line in enumerate(text):
            if line.startswith(STATE_START):
                break

            name_end = line.find(REGEX_NAME_END)
            name = line[1:name_end]
            regex_string = self.fix_regex_string(line[name_end + 2:], regex_string_list)

            regex_string_list.append(RegexString(name, regex_string))

        return regex_string_list

    # For a regular expression namedRegExs and a database of regular expressions RegExpressions
    # returns the fixed, final regular expression without named regular expressions inside
    def fix_regex_string(self, regex_string, fixed_regex_strings):
        for fixed_regex_string in fixed_regex_strings:
            regex_string = regex_string.replace(REGEX_NAME_START + fixed_regex_string.name + REGEX_NAME_END,
                                                REGEX_GROUP_START + fixed_regex_string.regex_string + REGEX_GROUP_END)
        return regex_string

    # Returns all identified stats in a list
    def get_states(self, text):
        return text[find_index_starting_with(text, STATE_START)][3:].split(' ')

    # Returns all identified entities in a list.
    def get_uniform_signs(self, text):
        return text[find_index_starting_with(text, SIGN_START)][3:].split(' ')

    # Returns a list of all commands in the form of tuples - (Starting state, regular expression, list of commands)
    def get_rules(self, text, regex_string_list):
        rules = list()
        rule_lines = text[find_index_starting_with(text, NAME_PREFIX):]

        while rule_lines:
            name_end_index = rule_lines[0].find(NAME_SUFFIX)
            starting_state = rule_lines[0][1:name_end_index]
            regex_string = self.fix_regex_string(rule_lines[0][name_end_index + 1:], regex_string_list)

            commands = list()
            for index, line in enumerate(rule_lines[2:]):
                if line == COMMAND_END:
                    rule_lines = rule_lines[index + 3:]
                    break
                commands.append(line)

            rules.append(Rule(starting_state, regex_string, commands))

        return rules

    def print(self):
        error_print("States:", self.states)
        error_print("Uniform signs:", self.signs)
        error_print("Rules:")

        for rule in self.rules:
            error_print(rule.starting_state + ", \"" + rule.regex_string + "\" " ":")
            for command in rule.commands:
                error_print(command)
            error_print()


class Generator:
    def __init__(self, data):
        self.data = data

    def generate(self, file):
        self.generate_imports(file)
        self.generate_rules(file)
        self.generate_algorithm(file)
        file.close()

    def generate_imports(self, file):
        file.write('from LAB1 import Lexer\n')
        file.write('\n')
        pass

    def generate_rules(self, file):
        file.write('rules = list()\n')
        file.write('\n')

        for rule in self.data.rules:
            file.write('commands = list()\n')
            for command in rule.commands:
                file.write('commands.append(\'' + command + '\')\n')

            if rule.regex_string.__contains__('\\'):
                rule.regex_string = rule.regex_string.replace('\\', '\\\\')
            if rule.regex_string.__contains__('\''):
                rule.regex_string = rule.regex_string.replace('\'', '\\\'')

            file.write('rules.append(Lexer.RegexRule(\'' +
                       rule.starting_state + '\', \'' + rule.regex_string + '\', commands))\n')
        file.write('\n')

    def generate_algorithm(self, file):
        file.write('program = Lexer.get_program_line()\n')
        file.write('lexer = Lexer.Lexer(rules, \'' + self.data.starting_state + '\')\n')
        file.write('Lexer.print_char_table(lexer.get_char_table(program))\n')
        file.write('\n')
        pass


generator_data = GeneratorData()
generator_data.get_data()
generator = Generator(generator_data)
if os.path.exists(LA_FILE_PATH):
    os.remove(LA_FILE_PATH)
LA_file = open(LA_FILE_PATH, 'a')
generator.generate(LA_file)
