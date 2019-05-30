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
        self.phone_number = phone_number
        self.filename = phone_number + '.talk'
        self.blocks = []
        self.history = []
        #Открываем файл на всю историю работы экземпляра класса
        try:
            self.talkfile = open(self.filename, 'r+')
            #Заносим всю историю нашего диалога
            self.history = self.get_history()
            #В списке history храниться история блоков
            #В history[0] - номер телефона абонента
        except FileNotFoundError:
            self.talkfile = open(self.filename, 'w')
            self.create_talk_file()
        
        return

    def __del__(self):
        """
        Деструктор класса
        """
        #Записываем и закрываем файл
        self.talkfile.close()

        return

    def save_talk(self, string, blockname='_АБ_'):
        """
        Записвыает разговор с абонентом в виде текстового протокола.

        param: string - строка текста, blockname - название блока
        return:
        """
        self.talkfile.write(blockname + ' > ' + string + '\n')
        #Игнорируем обозначение блока разговора абонента
        if (blockname != '_АБ_'):
            self.history.append(blockname)
        
        return

    @staticmethod
    def create_talk_file(self):
        """
        Вызывается скриптом, который запускается в начале разговора
        Вставляет номер телефона абонента в .talk файл
        """
        self.talkfile.write(self.phone_number + '\n')
        
        return
    
    def get_history(self):
        """
        Читаем протокол и забираем у него историю пройденных блоков
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


#Тест класса
if __name__ == "__main__":
    tr = TalkRecord('79123456789')
    print('Создаём файл протокола разговора', tr.filename)
    print('Симулирование разговора.')
    tr.save_talk('Hi!', '0000')
    tr.save_talk('hi')
    tr.save_talk('How are you?', '0001')
    tr.save_talk("I'm fine and you?")
    tr.save_talk("Good. I glad to see you!", '0003')
    tr.save_talk("I glad to see you too")
    print('Симуляция завершена. Файл создан. Можно посмотреть' \
          'результат')
    print('История блоков:')
    print(tr.history)
