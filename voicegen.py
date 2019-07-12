#!/usr/bin/python3
#Данная программа позволяет генерировать звуковые файлы, которые
#находятся в аудио-разделе блока речи.
#Эта программа предназначена для отладки диалогов при их написании
#Синтаксис запуска:
#python3 voicegen.py file1.trgs file2.trgs ...


from speechblock import SpeechBlock
from synthesis import Synthesis
import sys
import os

arguments = sys.argv
print(arguments.pop(0))
mypath = os.getcwd()
print(mypath)
files = []

for filename in arguments:
    sb = SpeechBlock(block=filename,  scheme='', path=mypath)
    for line in sb.audio_block:
        for key, elem in line.items():
            #в key находится имя файла назначенного в .trgs файле
            # fn содержит в себе название без расширения
            # raw - название .raw файла
            # transfert - содержит команду трансферта из raw в wav формат
            # для этого нужна утилита sox
            key = key.strip()
            fn = key.split('.')
            fn = fn[0]
            raw_file = fn + '.raw'
            files.append(fn)

            speech = Synthesis()
            print('raw_file =', raw_file)
            print('elem =', elem)
            speech.say(raw_file, elem)

for f in files:
    raw = f + '.raw'
    wav = f + '.wav'
    transfert = 'sox -r 8000 -b 16 -e signed-integer -c 1 ' + raw + ' ' + wav
    print(transfert)
    os.system(transfert)
    os.system('rm '+raw)    
