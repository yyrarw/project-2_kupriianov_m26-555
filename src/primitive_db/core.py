"""Основная логика базы данных: управление таблицами и CRUD-операции."""

from primitive_db.constants import (
    COLUMN_SEPARATOR,
    ID_COLUMN,
    ID_TYPE,
    NO_MATCHES_MSG,
    NO_TABLES_MSG,
    PYTHON_TYPES,
    RECORD_DELETED_MSG,
    RECORD_INSERTED_MSG,
    RECORD_UPDATED_MSG,
    TABLE_CREATED_MSG,
    TABLE_DROPPED_MSG,
    TABLE_EXISTS_MSG,
    TABLE_INFO_MSG,
    TABLE_NOT_FOUND_MSG,
    VALID_TYPES,
    VALUES_COUNT_MSG,
)
from primitive_db.parser import invalid


def format_columns(schema):
    """Возвращает схему таблицы строкой вида "ID:int, name:str"."""
    return ", ".join(
        f"{name}{COLUMN_SEPARATOR}{col_type}" for name, col_type in schema.items()
    )


def format_literal(value):
    """Показывает значение так, как его вводит пользователь: "Ann", 28, true."""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def parse_column(column, schema):
    """Разбирает описание столбца "имя:тип" с учетом уже добавленных столбцов."""
    name, separator, col_type = column.partition(COLUMN_SEPARATOR)
    is_valid = (
        separator
        and name.isidentifier()
        and name not in schema
        and col_type in VALID_TYPES
    )
    if not is_valid:
        raise invalid(column)
    return name, col_type


def get_table_schema(metadata, table_name):
    """Возвращает схему таблицы или выбрасывает KeyError, если таблицы нет."""
    if table_name not in metadata:
        raise KeyError(TABLE_NOT_FOUND_MSG.format(table_name))
    return metadata[table_name]


def check_value(col_type, value):
    """Проверяет, что значение соответствует типу столбца."""
    if type(value) is not PYTHON_TYPES[col_type]:
        raise invalid(format_literal(value))


def validate_clause(schema, clause):
    """Проверяет, что столбцы условия есть в таблице, а значения верного типа."""
    for column, value in clause.items():
        if column not in schema:
            raise invalid(column)
        check_value(schema[column], value)


def validate_set_clause(schema, clause):
    """Проверяет часть set: как условие, но столбец ID менять нельзя."""
    if ID_COLUMN in clause:
        raise invalid(ID_COLUMN)
    validate_clause(schema, clause)


def matches(row, where_clause):
    """Проверяет, подходит ли запись под условие."""
    return all(row.get(column) == value for column, value in where_clause.items())


def filter_rows(table_data, where_clause):
    """Возвращает записи, подходящие под условие."""
    return [row for row in table_data if matches(row, where_clause)]


def create_table(metadata, table_name, columns):
    """Создает таблицу со столбцом ID:int и столбцами columns."""
    if table_name in metadata:
        raise ValueError(TABLE_EXISTS_MSG.format(table_name))
    if not table_name.isidentifier():
        raise invalid(table_name)

    schema = {ID_COLUMN: ID_TYPE}
    for column in columns:
        name, col_type = parse_column(column, schema)
        schema[name] = col_type

    metadata[table_name] = schema
    print(TABLE_CREATED_MSG.format(table_name, format_columns(schema)))
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    get_table_schema(metadata, table_name)
    del metadata[table_name]
    print(TABLE_DROPPED_MSG.format(table_name))
    return metadata


def list_tables(metadata):
    """Печатает список всех таблиц."""
    if not metadata:
        print(NO_TABLES_MSG)
        return
    for table_name in metadata:
        print(f"- {table_name}")


def insert(metadata, table_name, values, table_data):
    """Проверяет значения и добавляет запись с новым ID в данные таблицы."""
    schema = get_table_schema(metadata, table_name)
    columns = [column for column in schema if column != ID_COLUMN]
    if len(values) != len(columns):
        raise invalid(VALUES_COUNT_MSG.format(len(columns), len(values)))
    for column, value in zip(columns, values):
        check_value(schema[column], value)

    new_id = max((row[ID_COLUMN] for row in table_data), default=0) + 1
    record = {ID_COLUMN: new_id, **dict(zip(columns, values))}
    table_data.append(record)
    print(RECORD_INSERTED_MSG.format(new_id, table_name))
    return table_data


def select(table_data, where_clause=None):
    """Возвращает все записи или только подходящие под условие."""
    if not where_clause:
        return list(table_data)
    return filter_rows(table_data, where_clause)


def update(table_data, table_name, set_clause, where_clause):
    """Обновляет поля set_clause у записей, подходящих под условие."""
    matched = filter_rows(table_data, where_clause)
    if not matched:
        print(NO_MATCHES_MSG.format(table_name))
    for row in matched:
        row.update(set_clause)
        print(RECORD_UPDATED_MSG.format(row[ID_COLUMN], table_name))
    return table_data


def delete(table_data, table_name, where_clause):
    """Удаляет записи, подходящие под условие, и возвращает оставшиеся."""
    matched = filter_rows(table_data, where_clause)
    if not matched:
        print(NO_MATCHES_MSG.format(table_name))
    for row in matched:
        print(RECORD_DELETED_MSG.format(row[ID_COLUMN], table_name))
    return [row for row in table_data if not matches(row, where_clause)]


def table_info(metadata, table_name, table_data):
    """Печатает столбцы таблицы и количество записей в ней."""
    schema = get_table_schema(metadata, table_name)
    print(TABLE_INFO_MSG.format(table_name, format_columns(schema), len(table_data)))
