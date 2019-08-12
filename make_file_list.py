#!/usr/bin/env python3

import os
import argparse
import codecs


def create_parser():
    '''Создаем и настраиваем парсер'''
    parser = argparse.ArgumentParser()
    parser.add_argument('directory_to_describe', nargs='?')
    parser.add_argument('directory_to_save', nargs='?')

    return parser


def parse_arguments(arguments):
    '''Разбираем аргументы и переназначаем в случае необходимости'''
    if arguments.directory_to_describe is None:
        arguments.directory_to_describe = os.getcwd()
    if arguments.directory_to_save is None:
        arguments.directory_to_save = arguments.directory_to_describe

    return arguments


def get_first_line(file_path):
    '''Добываем из файла первую строку'''
    file = codecs.open(file_path, 'r', 'cp1251')
    first_line = file.readline()

    return first_line


def create_file_list(directory_path):
    '''Создаем список файлов в данной директории'''
    file_list = os.listdir(directory_path)
    data_for_export = []
    # собираем нужные данные
    for file in file_list:
        path = os.path.join(directory_path, file)
        if os.path.isfile(path) and path[-3:] == 'txt':
            first_line = get_first_line(path)
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
    file_list = create_file_list(namespace.directory_to_describe)
    create_file(file_list, namespace.directory_to_save)


if __name__ == '__main__':
    main()