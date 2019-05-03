#!/usr/bin/python3

import sys


class Asterisk(object):
    """
    Класс для работы с Asterisk. Инкапсулирует в себе функции
    работы
    """
    def first_data_ignore(self):
        for _ in range(21):
            line = sys.stdin.readline()
        return

    def get_variable(self, variable):
        send_string = 'get variable ' + variable + '\n'
        sys.stdout.write(send_string)
        sys.stdout.flush()
        read_line = sys.stdin.readline()
        read_line = read_line.strip()
        return read_line[14:-1]

    def set_variable(self, name_variable, variable):
        send_string = 'set variable '
        send_string += str(name_variable)
        send_string += ' '
        send_string += str(variable)
        send_string += '\n'
        sys.stdout.write(send_string)
        sys.stdout.flush()
        read_line = sys.stdin.readline()
        return read_line
