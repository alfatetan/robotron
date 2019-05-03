#!/usr/bin/python3

import json
import sys
import pdb

# Коневертер для переработки пользовательского файла в необходимый
# формат  для описания блока речи
# Необходим пользовательский файл, который будет в себе содержать
# описание блока текста, согласно "Инструкции по составлению блоков речи"
# Пограмму лучше запускать с параметром, содержащим имя обрабатываемого
# файла. Формат:
# python3 converter.py file_name
# Параметр file_name - один
# Если есть желание использовать несколько файлов, то проще запустить
# этот скрипт через bash команду:
# find каталог -name *.txt -exec... (посмотреть в описании к find)

def open_file(filename):
    """
    Функция загрузки пользовательского файла в память
    """
    with  open(filename, 'r') as f_obj:
        file = f_obj.read()
    return file

def del_space(value):
    """
    Функция удаления лишних пробелов в полученных из файла данных
    """
    value = value.split(';')
    lst = []
    for el in value:
        lst.append(el.strip().lower())
    return lst

def save_block(filename, value):
    """
    Функция записи файла в нужном формате
    Согласно принятому стандарту, все файлы, содержащие триггерную часть
    имеют окончание .trgs
    """
    name = filename.split('.')
    filename = name[0]
    filename += '.trgs'
    with open(filename, 'w') as file:
        json.dump(value, file)
    return

def start_param():
    '''
    Определяем есть ли какой-либо параметр при запуске и присваиваем ему
    имя файла. Если нет такого параметра, то запрашиваем имя файла
    '''
    if len(sys.argv) == 1:
    #Если файл не был задан в параметрах вызова, тогда запросить имя файла
        filename = input('Введите название файла (можно с указанием пути: ')
    else:
        filename = sys.argv[1]
    return filename

def audio_separation(audio_block):
    '''
    Разделяем аудиоблок, чтобы в правильном формате занести всё в один
    словарь
    '''
    audio = {}
    for el in audio_block:
        key_value = el.split(';')
        if key_value != ['']:
            audio.update({key_value[0]:key_value[1]})
    block_file = {'_audio_': audio}
    return audio

def triggers_separation(triggers):
    '''
    Разделяем триггеры для правильной записи
    '''
    triggers_block = {}
    for el in triggers:
        if el:
            trigger = del_space(el)
            key = trigger.pop(0)
            value = tuple(trigger)
            triggers_block.update({key: value})

    return triggers_block



def main():
    '''
    Основной код программы
    '''
    #Запуск программы, если произошёл непосредственно её вызов
    filename = start_param()
    user_data = open_file(filename).split('$')
    #Выделяем аудиоблок (где описываются все аудиофайлы)
    audio_block = user_data.pop(0).split('\n')
    print(audio_block)
        
    audio = {}
    audio = audio_separation(audio_block)
    #А где запись содержимого аудио?
    
    #Выделяем триггеры
    triggers = user_data.pop(0).split('\n')

    triggers_block = {}
    triggers_block = triggers_separation(triggers)
    
    pdb.set_trace() #Запускаем отладку    
    all_file = audio + trigges_block
    save_block(filename, all_file)

    return True
    
if __name__ == '__main__':
    main()
