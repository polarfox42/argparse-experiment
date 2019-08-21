#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import argparse
import codecs
import configparser


def create_parser():
    '''
    Создаем и настраиваем парсер
    '''
    parser = argparse.ArgumentParser(
        description='''Программа для составления списка текстовых файлов
         в указанной директории''',
        add_help=False
    )
    args_group = parser.add_argument_group(title='Аргументы')
    options_group = args_group = parser.add_argument_group(title='Параметры')

    args_group.add_argument('describe', nargs='?',
                        help='Адрес директории для составления списка файлов')
    args_group.add_argument('save', nargs='?',
                        help='Адрес директории для сохранения файла со списком')
    options_group.add_argument('-c', '--coding', nargs='?', default='cp1251',
                        metavar='КОДИРОВКА',
                        help='Кодировка исходных файлов (по умолчанию "cp1251")')
    options_group.add_argument('--help', '-h', action='help', help='Справка')

    return parser


def get_config(path):
    '''
    Получаем параметры из файла конфигурации
    '''
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path)
    else:
        config = -1

    return config


def parse_arguments(arguments, config):
    '''
    Разбираем все возможные пути прихода аргументов, в приоритете командная строка.
    '''
    types = ['.py', '.txt', '.csv']
    report = 'report.txt'
    save = os.path.dirname(os.path.abspath(__file__))

    if isinstance(config, configparser.ConfigParser):
        config_types = config.get('Settings', 'types_list').split()
        config_types = [x.replace("'", '') for x in config_types]
        config_report = config.get('Settings', 'report_file_name')
        config_save = config.get('Settings', 'path_to_save')

        if config_types != '':
            types = config_types
        if config_report != '':
            report = config_report
        if config_save != '':
            save = config_save

    if arguments.describe is None:
        arguments.describe = os.path.dirname(os.path.abspath(__file__))
    if arguments.save is None:
        arguments.save = save

    return arguments, types, report


def get_first_line(file_path, coding):
    '''
    Добываем из файла первую строку
    '''
    file = codecs.open(file_path, 'r', coding)
    first_line = file.readline()

    return first_line


def create_file_list(directory_path, coding, knowing_types):
    '''Создаем список файлов в данной директории'''
    file_list = os.listdir(directory_path)
    data_for_export = []
    # собираем нужные данные
    for file in file_list:
        path = os.path.join(directory_path, file)
        ext = os.path.splitext(file)[1]
        if os.path.isfile(path) and ext in knowing_types:
            first_line = get_first_line(path, coding)
            data_for_export.append((file, first_line))

    return data_for_export


def create_file(data_list, path, output) -> None:
    '''Записываем в файл'''
    output = os.path.join(path, output)
    exp = codecs.open(output, 'w', 'utf-8')
    for data in data_list:
        exp.write(f'{data[0]}\t{data[1]}')
    print('Операция завершена.')


def main() -> None:
    '''
    Вызывается при запуске из консоли
    '''
    parser = create_parser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config = get_config(config_file)
    namespace = parser.parse_args()
    namespace, knowing_types, report = parse_arguments(namespace, config)
    file_list = create_file_list(namespace.describe, namespace.coding, knowing_types)
    create_file(file_list, namespace.save, report)


if __name__ == '__main__':
    main()
