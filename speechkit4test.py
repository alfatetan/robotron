#!/usr/local/bin/python3

class SpeechKit(object):
    """
    Тестовый класс, эмулирующий ответ от реального класса SpeechKit
    """
    def __init__(self):
        """
        Инициируем класс. По сути он будет пустым
        param:
        return:
        """
        self.result = ''
        return

    def recognize(self):
        """
        Принимаем текст от пользователя.
        param:
        return:
        """
        self.result = input('Слова абонента: ')
        return self.result
