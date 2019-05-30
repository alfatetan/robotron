#!/usr/bin/python3

import json
from agidebug import AgiDebug
#from talkrecord import TalkRecord

import pdb

class SpeechBlock(object):
    """
    Класс, отвечающий за работу блока речи
    """
    def __init__(self, block, scheme='my', skip=False,\
                 path=False):
        """
        Инициируем класс, где загружаем все необходимые данные
        """
        #pdb.set_trace()
        self.next_audiofile = ''
        self.next_audiotext = ''
        #Если путь не задан - выставляем стандартный
        if not path:
            #После можно сюда занести возможность подкачивать путь
            #из файла настроек
            path = '/var/lib/asterisk/sounds/'
        #Если нет расширения в названии блока, то добавим его сами
        if not block.count('.trgs'):
            #Если блок не содержит расширения, то добавим его
            self.trgs_filename = block + '.trgs'
        else:
            self.trgs_filename = block
        #Путь к схеме разговора
        self.scheme_folder = path + scheme
        #Имя файла блока с полным путём разговра
        self.trgs_filename = self.scheme_folder + self.trgs_filename
        
        #Считываем файл .trgs            
        try:
            with open(self.trgs_filename, 'r') as file:
                filedata = json.load(file)
            self.audio_block = filedata[0]
            self.triggers = filedata[1]
            #Основные свойства класса
            self.next_block = '' #Следующий блок
            self.skip = self.check_skip() #Проверка на пропуск блока

        except FileNotFoundError or FileExistsError:
            #Если проблемы с .trgs файлом, то завершаем разговор
            #Также обозначаем проблему в протоколе разговора
            self.sayfile = '_end'
            self.audio_block = [{'_end':'***Ошибка*** Файла .trgs нет'}]
            self.triggers = {'_end': '_'}
            self.skip = False
            print('Такого файла нет!!!')
        
        return

    def analysis(self, speech_text):
        """
        Анализируем сказанное и возвращаем следующий блок
        param: speech_text - распознанная речь
        return: название следующего блока, 
        """
        speech_text = ' ' + speech_text + ' '
        wt_max = 0
        best_block = ''
        default_block = ''
        print(self.triggers)
        #Чтобы определить следующий блок, перебираем триггеры
        for block, trigger in self.triggers.items():
            wt = 0
            for phrase in trigger:
                #Чтобы выделить слова отдельно - добавим пробелы
                word = ' ' + phrase[0] + ' '
                
                #Проверяем входит ли фраза в текст и сколько раз
                phrase_count = speech_text.count(word)
                
                if phrase_count:
                    wt += int(phrase[1]) * int(phrase_count)
                    #В зависимости от методики расчёта - альтернатива:
                    # wt += int(phrase[1])
                    
                #Заодно проверим - данный блок по дефолту или нет
                default_block = block if (phrase[0] == '_') else \
                    default_block

                #Ну и наличие безусловного перехода в другой блок
                #Может быть и пропустим, так как должны про него
                #знать заранее
                if phrase[0] == '*':
                    pass

            #Вычисляем лучший блок
            if wt > wt_max:
                #По логике самый первый блок из одинаковых будет
                #лучшим. Если хотим, чтобы был последний из
                #одинковых, нужно установить >= в условии
                wt_max = wt
                best_block = block

        #Если ничего не подошло, то используем значение по умолчанию
        best_block = default_block if not wt_max else best_block

        #Вычисление обратных переходов
        if best_block.count('back'):
            #Берём значение в скобках
            block = best_block.split('(')
            block = block[1].split(')')
            value = int(block[0])
            #Вызываем функцию расчёта предыдущих блоков
            best_block = 'back' + '=' + str(value)

        self.next_block = best_block
        
        return best_block

    def check_skip(self):
        """
        Проверяем, нужно ли пропускать выбранный блок
        param:
        return: self.skip = False / True
        """
        for block, trigger in self.triggers.items():
            self.skip = True if trigger[0].count('*') else False
            self.next_block = block if self.skip == True else \
                self.next_block

        return self.skip

    def get_audio(self, value=0):
        """
        Возвращает данные по следующему аудио
        param:
        return: dict(audiofile: audiotext)
        """
        #Проверяем сколько раз этот блок уже был и проигрываем
        #звуковой файл по очереди, повторяя по кольцу
        if value >= len(self.audio_block):
            value = value % len(self.audio_block)
        print('value = ', value)
        audio = self.audio_block[value]

        #Добавляем значение свойства в класс
        for key, text in audio.items():
            self.next_audiofile = key
            self.next_audiotext = text
            
        return audio

if __name__ == '__main__':
    #Тестируем класс
    myblock = '0003.trgs'
    myscheme = 'test_dialog/'
    s = SpeechBlock(block=myblock, scheme=myscheme,\
                    path='/Users/RyabovSergey/Projects/robotron/')
    speech_text = input('Enter the text:')
    s.analysis(speech_text)
    print ('Audiofile = ', s.get_audio(7))
    print ('check_skip = ', s.check_skip())
    print ('next_block = ', s.next_block)
    print ('next_audiofile = ', s.next_audiofile)
    print ('next_audiotext = ', s.next_audiotext)
    

