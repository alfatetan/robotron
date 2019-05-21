#!/usr/bin/python3

import 

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
        self.phone_number = phone_number
        self.filename = phone_number + '.talk'
        self.blocks = []
        #Открываем файл на всю историю работы экземпляра класса
        self.talkfile = open(self.filename, 'r+')
        #Заносим всю историю нашего диалога
        self.history = self.get_history()
        
        return

    def __del__(self):
        """
        Деструктор класса
        """
        #Записываем и закрываем файл
        self.file.close()

        return

    def save_talk(string, blockname='_АБ_'):
        """
        Записвыает разговор с абонентом в виде текстового протокола.

        param: string - строка текста, blockname - название блока
        return:
        """
        self.talkfile.write(blockname + ' > ' + string)
        #Игнорируем обозначение блока разговора абонента
        if (blockname != '_АБ_'):
            self.history.append(blockname)
        
        return

    def create_talk_file(self):
        """
        Вызывается скриптом, который запускается в начале разговора
        Вставляет номер телефона абонента в .talk файл
        """
        self.talkfile.write(self.phone_number + '\n')
        
        return
    
    def get_history(self):
        """
        Читаем протокол и забираем у него необходимые данные
        param:
        return:
        """
        blocks = []
        for line in self.talkfile:
            line = line.strip()
            line = line.split(' > ')
            block = line[0].strip()
            #Игнорируем "не блоки речи"
            if (block != '_АБ_'):
                blocks.append(block)

        return blocks

