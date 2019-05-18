#!/usr/bin/python3

import sys
from agidebug import AgiDebug

class Asterisk(object):
    """
    Класс для работы с Asterisk. Инкапсулирует в себе функции
    работы и все необходимые переменные
    """
    def __init__(self):
        #Пропускаем первые данные, которые нам не нужны
        self.first_data_ignore()

        #Подгружаем переменные с Asterisk
        self.scheme = self.get_variable('scheme')
        self.speech_block = self.get_variable('sayindex')
        self.skip = self.get_variable('skip')
        self.voicefile = self.get_variable('voicefile')
        self.waitvoice = self.get_variable('waitvoice')
        self.sayfile = ''
        
        return

    def __del__(self):
        """
        Диструктор объекта. В завершении мы выгружаем все имеющиеся
        данные в Asterisk
        """
        self.set_variable('scheme', self.scheme)
        self.set_variable('sayindex', self.speech_block)
        self.set_variable('skip', self.skip)
        self.set_variable('waitvoice', waitvoice)
        self.set_variable('sayfile', sayfile)

        return
    
    def first_data_ignore(self):
        """
        Пропускаем все начальные данные пришедшие от Asterisk
        """
        for _ in range(21):
            line = sys.stdin.readline()
            
        return

    def get_variable(self, variable):
        """
        Получаем значение переменной из Asterisk
        """
        send_string = 'get variable ' + variable + '\n'
        sys.stdout.write(send_string)
        sys.stdout.flush()
        read_line = sys.stdin.readline()
        read_line = read_line.strip()
        
        return read_line[14:-1]

    def set_variable(self, name_variable, variable):
        """
        Устанавливаем значение переменной в Asterisk
        """
        send_string = 'set variable '
        send_string += str(name_variable)
        send_string += ' '
        send_string += str(variable)
        send_string += '\n'
        sys.stdout.write(send_string)
        sys.stdout.flush()
        read_line = sys.stdin.readline()
        
        return read_line
    
#Проверка класса через AGI скрипт. Для этого необходимо этот файл
#назвать say_agi.agi и закинуть в папочку:
#/var/lib/asterisk/agi-bin/
#Протокол отладки будет храниться в class_asterisk.log
def test_class():
    """
    Проверка работоспособности класса
    """
    protocol = AgiDebug('class_asterisk.log')
    asterisk = Asterisk()
    protocol.upd('Создали экземпляр класса Asterisk')
    protocol.upd('При инициализации он пропускает первые данные')
    protocol.upd('Запрашиваем переменную sayfile диалплана Asterisk')
    variable = asterisk.get_variable('sayfile')
    protocol.upd(variable)
    protocol.upd('Самовольно заканчиваем разговор')
    asterisk.set_variable('sayfile', '_end')
    protocol.upd('Проверяем, установилась ли переменная:')
    protocol.upd(asterisk.get_variable('sayfile'))
    return

test_class()
