#!/usr/bin/python3

#Подключаем все необходимые классы и библиотеки
from asterisk import Asterisk
from speechkit import SpeechKit
from speechblock import SpeechBlock
from talkrecord import TalkRecord

#Отладочные библиотеки
#from asterisk4test import Asterisk
#from speechkit4test import SpeechKit
from agidebug import AgiDebug

#Основной текст AGI
#Связываемся с Asterisk и получаем необходимые переменные
asterisk = Asterisk()
log = TalkRecord(asterisk.abntnum)

#Читаем .trgs файл
sp_bl = SpeechBlock(block=asterisk.speech_block,\
                    scheme=asterisk.scheme,\
                    path='/Users/RyabovSergey/Projects/robotron/')

sk = SpeechKit()

#Проверяем есть ли значение skip, чтобы пропустить распознание
if not asterisk.skip:
    #Распознаём файл речи и получаем результат
    #sk.recognize(asterisk.voicefile)
    #Используем тестовый класс:
    sk.recognize()
    log.save_talk(sk.result)

#Определяем следующий блок
next_block_name = sp_bl.analysis(sk.result)

#Проверяем, если это относительный блок для того, чтобы вернуться
#на несколько шагов назад, то рассчитываем прошлый блок
if next_block_name.count('back='):
    next_block_name = next_block_name.split('=')
    next_block_name = (-1) * int(next_block_name[1]) - 1
    next_block_name = log.history[next_block_name]

#Читаем содержимое следующего блока и устанавливаем SKIP
sp_bl_next = SpeechBlock(block=next_block_name,\
                         scheme=asterisk.scheme,\
                         path='/Users/RyabovSergey/Projects/robotron/')

#Вычисляем следующий аудиофайл для воспроизведения
value = log.history.count(next_block_name)
next_audio = sp_bl_next.get_audio(value)

for audiofile, audiotext in next_audio.items():
    #Передаём адрес следующего аудиофайла
    asterisk.sayfile = audiofile
    #Делаем запись аудиотекста в протокол
    log.save_talk(string=audiotext, blockname=next_block_name)
    
#Если в новом блоке есть skip, то устанавливаем флаг на True
asterisk.skip = sp_bl_next.skip
asterisk.speech_block = next_block_name
#Передаём данные в Asterisk (должно сработать автоматически
#при вызове деструктора класса)
