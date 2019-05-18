#!/usr/bin/python3

class TalkRecord(object):
    """
    Класс, работающий с протоколом разговора и записывающим
    результаты в текстовом виде
    """
    def __init__(self, phone_number):
        """
        Инициализация класса. Читаем файл протокола и анализируем
        param:
        return:
        """
        self.filename = phone_number + '.talk'
        self.blocks = []
        #Открываем файл на всю историю работы экземпляра класса
        self.talkfile = open(self.filename, 'r+')
            
        return

    def __del__(self):
        """
        Деструктор класса
        """
        #Записываем и закрываем файл
        self.file.close()

    def read_records():
        """
        Читаем протокол и забираем у него необходимые данные
        param:
        return:
        """
        for line in self.talkfile:
            line = line.strip()
            line = line.split(' > ')
            block = line[0].strip()
            self.blocks.append(block)

        return


