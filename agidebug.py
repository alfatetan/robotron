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
        try:
            self.file = open(filename, 'a')
        except FileNotFoundError:
            self.file = open(filename, 'w')
        #Так как нам не нужна буферизация протокола, то нечего
        #тратить на это память
        return

    def __del__(self):
        """
        Закрываем файл в деструкторе
        """
        self.file.close()
        return

    def upd(self, *args):
        """Записываем в протокол полученное значение"""
        #with open(self.filename, 'a+') as file:
        for element in args:
            file.write(element)
        file.write('\n')
        return
        
if __name__ == '__main__':
    protocol = AgiDebug('protocol.txt')
    protocol.upd('Hi!')
    protocol.upd('How are you?')
