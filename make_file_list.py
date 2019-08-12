#!/usr/bin/env python3

import os
import argparse
import codecs


def create_parser():
    '''Создаем и настраиваем парсер'''
    parser = argparse.ArgumentParser(
        description = '''Программа для составления списка текстовых файлов 
        (.txt, .csv) в указанной директории''',
        add_help = False
    )
    args_group = parser.add_argument_group(title = 'Аргументы')
    options_group = args_group = parser.add_argument_group(title = 'Параметры')

    args_group.add_argument('describe', nargs='?',
                        help = 'Адрес директории для составления списка файлов')
    args_group.add_argument('save', nargs='?',
                        help = 'Адрес директории для сохранения файла со списком')
    options_group.add_argument('-c', '--coding', nargs='?', default = 'cp1251',
                        metavar = 'КОДИРОВКА',
                        help = 'Кодировка исходных файлов (по умолчанию "cp1251")')
    options_group.add_argument('--help', '-h', action = 'help', help = 'Справка')

    return parser


def parse_arguments(arguments):
    '''Разбираем аргументы и переназначаем в случае необходимости'''
    if arguments.describe is None:
        arguments.describe = os.getcwd()
    if arguments.save is None:
        arguments.save = arguments.describe

    return arguments


def get_first_line(file_path, coding):
    '''Добываем из файла первую строку'''
    file = codecs.open(file_path, 'r', coding)
    first_line = file.readline()

    return first_line


def create_file_list(directory_path, coding):
    '''Создаем список файлов в данной директории'''
    file_list = os.listdir(directory_path)
    data_for_export = []
    knowing_types = ['txt', 'csv']
    # собираем нужные данные
    for file in file_list:
        path = os.path.join(directory_path, file)
        if os.path.isfile(path) and path[-3:] in knowing_types:
            first_line = get_first_line(path, coding)
            data_for_export.append((file, first_line))

    return data_for_export


def create_file(data_list, path) -> None:
    '''Записываем в файл'''
    output_file = '!_directory_list.txt'
    output = os.path.join(path, output_file)
    exp = codecs.open(output, 'w', 'utf-8')
    for data in data_list:
        exp.write(f'{data[0]}\t{data[1]}')
    print('Операция завершена.')


def main() -> None:
    '''Вызывается при запуске из консоли'''
    parser = create_parser()
    namespace = parser.parse_args()
    namespace = parse_arguments(namespace)
    file_list = create_file_list(namespace.describe, namespace.coding)
    create_file(file_list, namespace.save)


if __name__ == '__main__':
    main()