"""Запуск приложения, основной цикл и разбор команд пользователя."""

import shlex

import prompt

from primitive_db.constants import (
    COMMAND_CREATE_TABLE,
    COMMAND_DROP_TABLE,
    COMMAND_EXIT,
    COMMAND_HELP,
    COMMAND_LIST_TABLES,
    INVALID_VALUE_MSG,
    KNOWN_COMMANDS,
    META_FILE,
    PROMPT_TEXT,
    UNKNOWN_COMMAND_MSG,
)
from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Печатает справку по командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def read_command():
    """Запрашивает команду; при Ctrl+D или Ctrl+C возвращает команду exit."""
    try:
        return prompt.string(PROMPT_TEXT)
    except (EOFError, KeyboardInterrupt):
        print()
        return COMMAND_EXIT


def execute_command(args, metadata, user_input):
    """Выполняет разобранную команду; возвращает False, если нужно выйти."""
    match args:
        case [command] if command == COMMAND_EXIT:
            return False
        case [command] if command == COMMAND_HELP:
            print_help()
        case [command] if command == COMMAND_LIST_TABLES:
            list_tables(metadata)
        case [command, table_name, *columns] if (
            command == COMMAND_CREATE_TABLE and columns
        ):
            if create_table(metadata, table_name, columns) is not None:
                save_metadata(META_FILE, metadata)
        case [command, table_name] if command == COMMAND_DROP_TABLE:
            if drop_table(metadata, table_name) is not None:
                save_metadata(META_FILE, metadata)
        case [command, *_] if command in KNOWN_COMMANDS:
            print(INVALID_VALUE_MSG.format(user_input))
        case [command, *_]:
            print(UNKNOWN_COMMAND_MSG.format(command))
    return True


def run():
    """Запускает основной цикл работы с базой данных."""
    print("***База данных***")
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = read_command().strip()
        try:
            args = shlex.split(user_input)
        except ValueError:
            print(INVALID_VALUE_MSG.format(user_input))
            continue
        if args and not execute_command(args, metadata, user_input):
            break
