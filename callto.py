#!/usr/bin/python3
#Формирует звонок
#Номер телефона передаётся в командной строке

import sys
import os

class CallFiles(object):
    '''
    Класс, создающий и копирующий Call File
    '''
    def __init__(self, phones=[], scheme='my', startblock='0000'):
        """
        Инициируем класс
        """
        if not phones:
            self.phones = []
        else:
            self.phones = phones
            
        if not scheme:
            self.scheme = 'my'
        else:
            self.scheme = scheme
            
        if not startblock:
            self.startblock = 0000
        else:
            self.startblock = startblock
            
        self.callfile = []

        return

    def phone_append(self, phone):
        """
        Добавляем номер в список
        """
        self.phones.append(phone)
        return

    def change_scheme(self, scheme):
        """
        Установка схемы диалога
        """
        self.scheme = scheme
        return

    def set_startblock(self, start):
        """
        Установка стартового блока
        """
        self.startblock = start
        return

    def create_call_file(self, phone):
        """
        Создаём файл .call для активации звонка
        """
        filename = str(phone)+'.call'
        self.callfile = [
            'Channel: SIP/'+str(phone)+'@590889',
            'MaxRetries: 3',
            'RetryTime: 10',
            'Context: zadarma-in',
            'Extension: 590889',
            'Set: abntnum='+str(phone),
            'Set: startblock='+str(self.startblock),
            'Set: scheme='+str(self.scheme),
            'Priority: 1'
        ]
        with open(filename, 'w') as file:
            for line in self.callfile:
                file.write(line+'\n')
        
        return
    
    def create_call_files(self):
        for phone in self.phones:
            self.create_call_file(phone)
        return

    
def help_me():
    print('Формат использования команды callto.py:')
    print('python3 callto.py [scheme=<имя схемы>] [startblock=<' \
          'начальный блок>] <номер_телефона1> ... <номер_телефонаN>')
    print('Между параметрами и символом "=" не должно быть пробелов.')
    print('Телефоны должны начинаться с кода страны без символа "+"')
    print('Для России необходим формат: 79123456789')
    return

#Обрабатываем параметры, необходимые для наших call файлов
def start():
    dotcalls = CallFiles()
    arguments = sys.argv
    arguments.pop(0)
    for line in arguments:
        if line.count('start') or line.count('startblock'):
            line = line.split('=')
            start = line[1].strip()
            dotcalls.set_startblock(start)
        elif line.count('scheme') or line.count('dialog'):
            line = line.split('=')
            scheme = line[1].strip()
            dotcalls.change_scheme(scheme)
        elif line.count('--help'):
            help_me()
        else:
            try:
                phone = int(line.strip())
                dotcalls.phone_append(str(phone))
            except ValueError:
                print('Ошибка в параметре номера телефона!')
                break

    dotcalls.create_call_files()
    return

start()
os.system('mv *.call /var/spool/asterisk/outgoing')
