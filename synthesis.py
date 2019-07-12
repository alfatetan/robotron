import json
import requests

class Synthesis(object):
    """
    Класс синтезирования голоса с помощью Yandex SpeechKit
    """
    def __init__(self, folder_id='b1gfll967nmtrqvfc2v5',  lang='ru-RU', \
                 type_voice = 'female', 
    ):
        """
        Инициируем класс с первоначальными данными для синтеза
        param:
        return:
        """
        self.folder_id =  folder_id
        self.iam_token = self.get_token(path='/Users/RyabovSergey/Projects/robotron/')

        self.url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        self.headers = {
            'Authorization': 'Bearer ' + self.iam_token,
            }
        self.speed = '1.0'
        self.data = {
            'text': '',
            'lang': lang,
            'folderId': self.folder_id,
            'voice': 'oksana',
            'emotion': 'neutral',
            'speed': self.speed,
            'format': 'lpcm',
            'sampleRateHertz': '8000',
            }
        return

    def voice_gen(self):
        """
        Гененрируем ответ с сервера
        param:
        return:
        """
        with requests.post(self.url, headers=self.headers, data=self.data, \
                           stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: " \
                            "code:%d, message: %s" % (resp.status_code, resp.text))
            for chunk in resp.iter_content(chunk_size=None):
                yield chunk
        return

    def say(self, filename, text, who='oksana', attitude='neutral'):
        """
        Генерируем аудиофайл
        param: text - сам текст
        return: звуковой файл lpcm формата (wav без заголовка)
        """
        self.data['voice'] = who
        self.data['emotion'] = 'neutral'
        self.data['speed'] = self.speed
        self.data['text'] = text

        with open(filename, 'wb') as new_file:
            for audio_content in self.voice_gen():
                new_file.write(audio_content)

        return

    def say_evil(self, text, who='oksana'):
        """
        Говорим со злой интонацией
        param:
        return:
        """
        self.say(text, who, attitude='evil')
        return

    def say_good(self, text, who='oksana'):
        """
        Говорим со злой интонацией
        param:
        return:
        """
        self.say(text, who, attitude='good')
        return

    def change_speed(self, persent):
        """
        Устанавливает скорость в процентах
        param: persent - 100 нормальная скорость речи
        минимально 10 и 300 максимально
        return:
        """
        persent = persent / 100
        self.speed = str(persent)
        return

    @staticmethod
    def get_token(filename='iam.token', \
                  path='/var/lib/asterisk/agi-bin/'):
        """
        Загружаем IAM токен для распознавания звукового файла, по умолчанию
        это файл iam.token
        :return: False, если не будет iam.token
        """
        filename = path + filename
        
        with open(filename, 'r') as file:
            full_token = json.load(file)
        return full_token['iamToken']


if __name__ == '__main__':
    speech = Synthesis()
    speech.say('mytest.raw', 'Привет, мой дорогой друг! З+амок и зам+ок')
