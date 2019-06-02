#Подготавливает файлы для конвертирования
import sys

filename = sys.argv[1]
with open (filename) as file:
    filedata = file.read()

filedata = filedata.split('%%%')
for each_file in filedata:
    each_file.strip()
    each_file = each_file.split('+++')
    with open (each_file[0].strip(), 'w') as new_file:
        new_file.write(each_file[1].strip())
