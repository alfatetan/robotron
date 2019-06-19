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
        self.callerid = self.first_data_ignore()
        if self.callerid.count('unknown'):
            self.abntnum = self.get_variable('abntnum')
            self.typering = 'out'
        else:
            self.abntnum = self.callerid
            self.typering = 'in'

        self.scheme = self.get_variable('scheme')
        self.speech_block = self.get_variable('sayindex')

        skip = self.get_variable('skip')
        self.skip = False if skip.count('0') else True
        
        self.voicefile = self.get_variable('voicefile')
        self.waitvoice = self.get_variable('waitvoice')
        self.sayfile = ''

        return

    def __del__(self):
        """
        Деструктор объекта. В завершении мы выгружаем все имеющиеся
        данные в Asterisk
        """
        if self.scheme:
            self.set_variable('scheme', self.scheme)
        if self.speech_block:
            self.set_variable('sayindex', self.speech_block)
        self.set_variable('skip', str(int(self.skip)))
        self.set_variable('waitvoice', self.waitvoice)
        if self.sayfile.count('.wav'):
            self.sayfile = self.sayfile.split('.')
            self.sayfile = self.sayfile[0]
        self.set_variable('sayfile', self.sayfile)
        self.set_variable('audiorec', self.abntnum)

        return
    
    def first_data_ignore(self):
        """
        Пропускаем все начальные данные пришедшие от Asterisk
        и возвращаем callerid абонента. Если звонок исходящий
        то это значение будет unknown, если входящий, то в нём
        будет номер телефонаnn
        """
        for _ in range(21):
            line = sys.stdin.readline()
            if line.count('agi_callerid'):
                line = line.split(':')
                callerid = line[1].strip()
            
        return callerid.lower()

    def get_variable(self, variable):
        """
        Получаем значение переменной из Asterisk
        """
        send_string = 'get variable ' + variable + '\n'
        sys.stdout.write(send_string)
        sys.stdout.flush()
        read_line = sys.stdin.readline()
        read_line = read_line.strip()
        if read_line.count('result=1'):
            read_line = read_line[14:-1]
        else:
            read_line = False
            
        return read_line

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

    def hungup(self):
        """
        Вешаем трубку
        """
        sys.stdout.write('hungup')
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
    protocol = AgiDebug('/var/lib/asterisk/agi-bin/class_asterisk.log')
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

if __name__ == "__main__":
    test_class()
