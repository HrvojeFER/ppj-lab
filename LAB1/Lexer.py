from __future__ import print_function
from LAB1 import Regex
import sys

STARTING_STATE = [0]
EMPTY_STATE = []
FLUSH = '-'
NEW_LINE = 'NOVI_REDAK'
ENTER_STATE = 'UDJI_U_STANJE'
RETURN = 'VRATI_SE'
HRVOJE_JE_SMIJEŠAN = 'TVOJA STARA\n'


# Prints to standard error output
def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_program_line():
    program_line = ''

    for line in sys.stdin:
        if line == HRVOJE_JE_SMIJEŠAN:
            break
        for char in line:
            program_line += char

    return program_line


def print_char_table(char_table):
    for char in char_table:
        print(char.uniform_sign, char.line_no, char.group)


class Char:
    def __init__(self, uniform_sign, line_no, group):
        self.uniform_sign = uniform_sign
        self.line_no = line_no
        self.group = group


class RegexRule:
    def __init__(self, starting_state, regex_string, commands):
        self.starting_state = starting_state
        self.regex = Regex.RegularExpression(regex_string)
        self.commands = commands
        self.state = STARTING_STATE


class Lexer:
    def __init__(self, rules, starting_state):
        self.rules = rules
        self.current_state = starting_state

        self.char_table = list()
        self.no_lines = 1

        self.end = 0
        self.start = 1
        self.last_match = self.end

        self.reset_rule_states()
        self.matching_rule_index = None

    def lexer_transition(self, sign):
        for rule in self.rules:
            if self.current_state == rule.starting_state:
                rule.state = rule.regex.transition(rule.state, sign)
            else:
                rule.state = EMPTY_STATE

    def reset_rule_states(self):
        for rule in self.rules:
            rule.state = STARTING_STATE
        self.lexer_transition(Regex.EPSILON)

    def rule_states_empty(self):
        for rule in self.rules:
            if rule.state != EMPTY_STATE:
                return False

        return True

    def get_matching_rule_index(self):
        for index, rule in enumerate(self.rules):
            if rule.state.__contains__(1):
                return index
        return -1

    def matching_rule_exists(self):
        for rule in self.rules:
            if rule.state.__contains__(1):
                return True
        return False

    def enter_state(self, state):
        self.current_state = state

    def reset(self):
        self.char_table = list()
        self.no_lines = 1

        self.end = 0
        self.start = 1
        self.last_match = self.end

        self.reset_rule_states()
        self.matching_rule_index = None

    def do_commands(self, group):
        uniform_sign = None
        has_new_line_command = False

        for command in self.rules[self.matching_rule_index].commands:
            if command == FLUSH:
                pass
            elif command == NEW_LINE:
                has_new_line_command = True
                self.no_lines += 1
            elif command.startswith(ENTER_STATE):
                new_state = command.replace(ENTER_STATE + ' ', '')
                self.enter_state(new_state)
            elif command.startswith(RETURN):
                to_ret = int(command.replace(RETURN + ' ', ''))
                self.last_match += to_ret - len(group)
                group = group[:to_ret - len(group)]
            else:
                uniform_sign = command

        if not has_new_line_command and group.__contains__('\n'):
            self.no_lines += 1

        if uniform_sign:
            self.char_table.append(Char(uniform_sign, self.no_lines, group))

    def get_char_table(self, program):
        self.reset()

        while True:
            if not self.rule_states_empty():
                current_sign = program[self.end]
                self.end += 1
                self.lexer_transition(current_sign)

                if self.end >= len(program):
                    if self.matching_rule_index:
                        group = program[self.start - 1:self.last_match]
                        self.do_commands(group)
                        break

                    else:
                        if self.start >= len(program):
                            break
                        error = program[self.start]
                        self.end = self.start
                        self.start += 1
                        error_print(error)
                        continue

                if self.matching_rule_exists():
                    self.matching_rule_index = self.get_matching_rule_index()
                    self.last_match = self.end

            else:
                if self.matching_rule_index:
                    group = program[self.start - 1:self.last_match]
                    self.do_commands(group)

                    self.start = self.last_match + 1
                    self.end = self.last_match

                else:
                    if self.start >= len(program):
                        break

                    error = program[self.start]
                    self.end = self.start
                    self.start += 1
                    error_print(error)

                self.reset_rule_states()
                self.matching_rule_index = None

        return self.char_table
