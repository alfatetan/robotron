#!/usr/bin/python3
import json
import urllib.request


class SpeechKit(object):
    """
    Класс, работающий с Yandex Speech Kit и перерабатывающий звук в текст
    """
    def __init__(self, folder_id='b1gfll967nmtrqvfc2v5'):
        """
        Создание экземпляра класса
        """
        self.iam_token = self.get_token()
        self.folder_id = folder_id
        self.params = "&".join([
            "topic=general",
            "folderId=%s" % self.folder_id,
            "lang=ru-RU",
            "format=lpcm",
            "sampleRateHertz=8000"
        ])
        self.result = ''

    @staticmethod
    def get_token(filename='iam.token'):
        """
        Загружаем IAM токен для распознавания звукового файла, по умолчанию
        это файл iam.token
        :return: False, если не будет iam.token
        """
        with open(filename, 'r') as file:
            full_token = json.load(file)
        return full_token['iamToken']

    def recognize(self, filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
        except FileExistsError:
            return False
        except FileNotFoundError:
            return False

        url = urllib.request.Request(
            "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" %
            self.params, data=data)
        url.add_header("Authorization", "Bearer %s" % self.iam_token)

        response_data = urllib.request.urlopen(url).read().decode('UTF-8')
        decoded_data = json.loads(response_data)

        if decoded_data.get("error_code") is None:
            self.result = decoded_data.get("result")

        return self.result

    def get_result(self):
        return self.result


if __name__ == "__main__":
    speech = SpeechKit()
    speech.recognize('sounds/name.wav')
    print(speech.get_result())
