#!/usr/bin/python3

class AgiDebug:
    """
    Класс отладки работы AGI скрипта
    """
    def __init__(self, filename=False):
        defaultpath = '/var/lib/asterisk/agi-bin/protocol.txt'
        self.filename = defaultpath if not filename else filename
        #Параметр 0 обозначает что не используем буферизацию
        #Параметр 1 и более - количество буферизуемых строк
        #Отрицательное значение - используем по величине системного
        #буфера (см параметр open)
        self.file = open(filename, 'a+')
        #Так как нам не нужна буферизация протокола, то нечего
        #тратить на это память
        return

    def __del__(self):
        """
        Закрываем файл в деструкторе
        """
        self.file.close()
        return

    def append(self, *args):
        """Записываем в протокол полученное значение"""
        for element in args:
            element += '\n'
            self.file.write(element)
        return
        
if __name__ == '__main__':
    protocol = AgiDebug('protocol.txt')
    protocol.append('Hi!')
    protocol.append('How are you?')
