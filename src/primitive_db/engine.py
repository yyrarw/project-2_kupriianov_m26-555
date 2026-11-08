"""Запуск приложения, основной цикл и обработка команд пользователя."""

import prompt
from prettytable import PrettyTable

from primitive_db import constants as const
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    get_table_schema,
    insert,
    list_tables,
    select,
    table_info,
    update,
    validate_clause,
    validate_set_clause,
)
from primitive_db.parser import (
    invalid,
    parse_args,
    parse_delete,
    parse_insert,
    parse_select,
    parse_update,
)
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Печатает справку по командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
        " - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение>"
        " - прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1>"
        " where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение>"
        " - удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def print_rows(schema, rows):
    """Печатает записи таблицей PrettyTable в порядке столбцов схемы."""
    if not rows:
        print(const.NO_RECORDS_MSG)
        return
    table = PrettyTable()
    table.field_names = list(schema)
    for row in rows:
        table.add_row([row[column] for column in schema])
    print(table)


def ensure_no_args(text):
    """Проверяет, что у команды нет лишних аргументов."""
    if text:
        raise invalid(text)


def invalid_command(command, text):
    """Создает исключение о некорректных аргументах команды."""
    return invalid(f"{command} {text}".strip())


def parse_table_name(command, text):
    """Возвращает единственный аргумент команды — имя таблицы."""
    args = parse_args(text)
    if len(args) != 1:
        raise invalid_command(command, text)
    return args[0]


def handle_create_table(metadata, text):
    """create_table <имя_таблицы> <столбец:тип> ..."""
    args = parse_args(text)
    if len(args) < 2:
        raise invalid_command(const.COMMAND_CREATE_TABLE, text)
    table_name, *columns = args
    create_table(metadata, table_name, columns)
    save_metadata(const.META_FILE, metadata)
    save_table_data(table_name, [])


def handle_drop_table(metadata, text):
    """drop_table <имя_таблицы>"""
    table_name = parse_table_name(const.COMMAND_DROP_TABLE, text)
    drop_table(metadata, table_name)
    save_metadata(const.META_FILE, metadata)
    delete_table_data(table_name)


def handle_insert(metadata, text):
    """insert into <имя_таблицы> values (...)"""
    table_name, values = parse_insert(text)
    table_data = load_table_data(table_name)
    insert(metadata, table_name, values, table_data)
    save_table_data(table_name, table_data)


def handle_select(metadata, text):
    """select from <имя_таблицы> [where <столбец> = <значение>]"""
    table_name, where_clause = parse_select(text)
    schema = get_table_schema(metadata, table_name)
    if where_clause:
        validate_clause(schema, where_clause)
    rows = select(load_table_data(table_name), where_clause)
    print_rows(schema, rows)


def handle_update(metadata, text):
    """update <имя_таблицы> set <столбец> = <значение> where <условие>"""
    table_name, set_clause, where_clause = parse_update(text)
    schema = get_table_schema(metadata, table_name)
    validate_set_clause(schema, set_clause)
    validate_clause(schema, where_clause)
    table_data = load_table_data(table_name)
    update(table_data, table_name, set_clause, where_clause)
    save_table_data(table_name, table_data)


def handle_delete(metadata, text):
    """delete from <имя_таблицы> where <столбец> = <значение>"""
    table_name, where_clause = parse_delete(text)
    schema = get_table_schema(metadata, table_name)
    validate_clause(schema, where_clause)
    table_data = delete(load_table_data(table_name), table_name, where_clause)
    save_table_data(table_name, table_data)


def handle_info(metadata, text):
    """info <имя_таблицы>"""
    table_name = parse_table_name(const.COMMAND_INFO, text)
    table_info(metadata, table_name, load_table_data(table_name))


def execute_command(metadata, user_input):
    """Выполняет команду пользователя; возвращает False, если нужно выйти."""
    command, _, text = user_input.partition(" ")
    text = text.strip()
    match command:
        case const.COMMAND_EXIT:
            ensure_no_args(text)
            return False
        case const.COMMAND_HELP:
            ensure_no_args(text)
            print_help()
        case const.COMMAND_LIST_TABLES:
            ensure_no_args(text)
            list_tables(metadata)
        case const.COMMAND_CREATE_TABLE:
            handle_create_table(metadata, text)
        case const.COMMAND_DROP_TABLE:
            handle_drop_table(metadata, text)
        case const.COMMAND_INSERT:
            handle_insert(metadata, text)
        case const.COMMAND_SELECT:
            handle_select(metadata, text)
        case const.COMMAND_UPDATE:
            handle_update(metadata, text)
        case const.COMMAND_DELETE:
            handle_delete(metadata, text)
        case const.COMMAND_INFO:
            handle_info(metadata, text)
        case _:
            print(const.UNKNOWN_COMMAND_MSG.format(command))
    return True


def read_command():
    """Запрашивает команду; при Ctrl+D или Ctrl+C возвращает команду exit."""
    try:
        return prompt.string(const.PROMPT_TEXT).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return const.COMMAND_EXIT


def run():
    """Запускает основной цикл работы с базой данных."""
    print("***База данных***")
    print_help()
    while True:
        metadata = load_metadata(const.META_FILE)
        user_input = read_command()
        if not user_input:
            continue
        try:
            if not execute_command(metadata, user_input):
                break
        except (KeyError, ValueError) as error:
            print(error.args[0])
