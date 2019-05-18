#!/usr/local/bin/python3

import json
from agidebug import AgiDebug

class SpeechBlock(object):
    """
    Класс, отвечающий за работу блока речи
    """
    def __init__(self, trgs_filename):
        """
        Инициируем класс, где загружаем все необходимые данные
        """
        #Если нет расширения в названии блока, то добавим его сами
        if not trgs_filename.count('.trgs'):
            trgs_filename += '.trgs'

        #Считываем файл .trgs            
        try:
            with open(filename, 'r') as file:
                filedata = json.load(file)
            self.audio_block = filedata[0]
            self.triggers = filedata[1]
        except:
            #Если проблемы с .trgs файлом, то завершаем разговор
            #Также обозначаем проблему в протоколе разговора
            self.sayfile = '_end'
            self.audio_block = [{'_end':'****Ошибка**** Файла .trgs нет'}]
            self.triggers = []
        
        
        return
    

