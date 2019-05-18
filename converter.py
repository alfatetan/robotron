#!/usr/bin/python3
# Конвертер по работе с пользовательскими файлами и перевод их в
# формат, необходимый для работы системы.

import sys
import os
import json
#import pdb

def check_start_args():
    '''
    Проверяем есть ли аргументы. Если нет, то запрашиваем имя файла
    '''
    if len(sys.argv) == 1:
        # arg = input('Введите название файла(ов) и/или параметры : ')
        # args.append(arg)
        print('Введите параметры при запуске конвертера.')
        return False
    else:
        args = sys.argv[1:]
    #Проверка аргументов
    keys = []
    filenames = []
    for el in args:
        if el.count('--'):
            keys.append(el)
        else:
            filenames.append(el)
    args = {
        'filenames':filenames,
        'keys':keys,
    }
    return args

def help_converter():
    print('\n\nКонвертер для переработки пользовательского файла в ' \
          'необходимый формат для описания блока речи.\n' \
          'Необходимо указать имена пользовательского(их) файла(ов),'\
          ' которые будут содержать в себе описание блока текста, ' \
          'текста, согласно "Инструкции по составлению блоков речи"' \
          '\n\tФормат команды:\n' \
          'python3 converter [keys] [file_name [file_namse]]')
    return True

def keys_calls(keys_list):
    '''
    Обрабатываем параметры ключей
    '''
    #Пока работаем с одним ключом: --help
    if keys_list.count('--help'):
        help_converter()
        return False
    return True

def open_user_file(filename):
    '''
    Загружаем пользовательский файл
    '''
    with open(filename, 'r') as file:
        filedata = file.read()
        print("\n\t\tСодержание файла пользователя")
        print(filedata)
        print('*'*50)
    return filedata

def save_trgs_file(filename, variable):
    '''
    Записываем сформированный файл
    '''
    filename = filename.split('.')
    filename = filename.pop(0)
    filename += '.trgs'
    with open(filename, 'w') as file:
        json.dump(variable, file)
    print('Файл ', filename, 'сформирован и записан.')
    print('*'*50)
    return True

def delete_empty(lst):
    """
    Удаляем пустые значения из списка
    """
    while lst.count(''):
        lst.remove('')
    return lst
    
def audio_formating(audio_data):
    '''
    Обработка и форматирование аудиоблока в пользовательском файле
    '''
    audio_block = {}
    audio_data = audio_data.split('\n')
    audio_data = delete_empty(audio_data)
    for line in audio_data:
        line = line.split(':')
        key = line[0].strip()
        value = line[1].strip()
        # value = 'RT > ' + value
        audio_block.update({key:value})
    return audio_block

def weighting(phrase):
    '''
    Взвешиваем полученную фразу
    '''
    all_wt = 0 #Общий вес выражения
    #Фраза может состоять из одного слова, а может из нескольких
    #В любом случае проведём это все через цикл и, если фраза будет
    #иметь всего одно слово, значит и цикл будет из одного действия
    words = []
    if phrase.count('"'):
        if phrase.count('"('):
            #Если выражение имеет общий вес, то просто возвращаем его
            words = phrase.split('"(')
            #Убираем последнюю скобку
            all_wt = int(words[1][:-1])
            return all_wt
        #Убираем кавычки
        phrase = phrase[1:-1]
        words = phrase.split() #Получаем список слов
        words = delete_empty(words)
    else:
        words.append(phrase)
    #Подсчитываем вес слов
    for word in words:
        if word.count('('):
            #Если указан вес - добавляем его в общий вес фразы
            word = word.split('(')
            all_wt += int(word[1][:-1])
        else:
            #Иначе - инкрементируем значение веса по количеству слов
            all_wt += 1
    return all_wt

def clearing(phrase):
    '''
    Очищаем фразу от ненужных символов и подгатавливаем к картели
    '''
    words = []
    word = ''
    if phrase.count('"'):
        phrase = phrase.split()
        for el in phrase:
            if el.count('('):
                el = el.split('(')
                words.append(el[0])
            else:
                words.append(el)
        #Собираем фразу заново
        phrase = ' '.join(words)
        #Убираем кавычки
        phrase = phrase[1:-1]
        return phrase
    elif phrase.count('('):
        words = phrase.split('(')
        phrase = words[0]
        return phrase
    if phrase.count(',') or phrase.count('.') or phrase.count('!') \
       or phrase.count('?'):
        print('\n\tПРЕДУПРЕЖДЕНИЕ!!! Обратите внимание, возможно есть '
              'ошибки в пользовательском файле!!! (знаки препинания)')
    return phrase

def words_separate(line):
    '''
    Разделяем слова и выражения и возвращаем словарь картелей
    с весом каждого слова
    '''
    line = str(line[0])
    #Разбиваем строку по пробелам и получаем список слов
    line_lst = line.split()
    line_lst = delete_empty(line_lst)
    phrases = [] #Отформатированный список фраз
    word = '' #Временная переменная, хранящая слово в кавычках
    flag = False #Флаг того, что фраза не закончена (кавычки)

    for el in line_lst:
        if el.count('"'):
            flag = not flag
        word += el + (' ' * flag)
        if not flag:
            #так как для распознания используется только нижний
            #регистр - сразу же используем его
            phrases.append(word.lower())
            word = ''

    #Удаляем пустые строки в списке, на всякий случай
    phrases = delete_empty(phrases)    
    #В phrases находится разбитые и необработанные фразы со всеми
    #спецсимволами (кавычками и скобками)

    phrases_format = []
    for el in phrases:
        #Взвешиваем их и убираем ненужные символы
        wt = weighting(el) #взвешиваем фразу
        phrase = clearing(el) #очищаем фразу от ненужных элементов
        #Переберём полученный результат и создадим картели, опираясь на
        #весА полученных фраз
        phrases_format.append((phrase,wt)) 
        
    return phrases_format

def triggers_formating(triggers_data):
    '''
    Форматируем блок триггеров читая из файла пользователя
    и переводя в необходимый формат
    '''
    triggers_data = triggers_data.split('\n')
    triggers_data = delete_empty(triggers_data)
    triggers_block = {}
    for line in triggers_data:
        line = line.split(':')
        #Выделяем название блока, который будет ключём в словаре
        block_name = line.pop(0)
        block_name = block_name.strip()
        #Разделяем слова и выражения, выставляя веса
        words = words_separate(line)
        #Проверяем, занят ли ключ другими значениями и, если занят
        #Добавляем полученные выражения к тому же ключу
        if block_name in triggers_block:
            temp_value = triggers_block.pop(block_name)
            for word in words:
                if word not in temp_value:
                    temp_value.append(word)
            triggers_block.update({block_name: temp_value})
        else:
            triggers_block.update({block_name: words})

    return triggers_block

def convert_file(file_name):
    '''
    Конвертирование файла пользователя
    '''
    #Открываем файл и загружаем содержимое
    filedata = open_user_file(file_name)

    #Отделяем блок аудиоблок от блока триггеров
    filedata = filedata.split('$')
    
    #Обрабатываем аудиоблок
    audio_block = audio_formating(filedata[0])

    #Обрабатываем блок триггеров
    triggers_block = triggers_formating(filedata[1])
    #Записываем файл в формат trgs
    all_trgs_file = (
        audio_block,
        triggers_block,
    )
    save_trgs_file(file_name, all_trgs_file)
    
    return 

def converter():
    '''
    Запускаем конвертер
    '''
    #pdb.set_trace()
    #Проверяем наличие аргументов
    args = check_start_args()
    if not args:
        #Если нет аргументов - выходим
        print('Введите аргументы при вызове конвертора')
        return
    #Если есть ключи, то обрабатываем
    if len(args['keys']):
        keys_result = keys_calls(args['keys'])
        if not keys_result:
            #Если ключ завершает конвертер, то выходим
            return
    #Перебираем 
    for filename in args['filenames']:
        convert_file(filename)
    return
        
def test():
    """
    Tests
    """
    print('*'*50)
    print('Test word_separate function:')
    line = 'My "GENERAL(5) sentance" for? my(2) "SpECiaL test"(11) '\
        'because "I WANT" to see how thiS WORK'
    print('IN: ',line)
    result = words_separate(line)
    print(result)
    print('='*50)
    return
    
if __name__== "__main__":
#    test()
    converter()
