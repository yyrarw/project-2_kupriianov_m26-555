"""Основная логика базы данных: управление таблицами."""

from primitive_db.constants import (
    COLUMN_SEPARATOR,
    ID_COLUMN,
    ID_TYPE,
    INVALID_VALUE_MSG,
    NO_TABLES_MSG,
    TABLE_CREATED_MSG,
    TABLE_DROPPED_MSG,
    TABLE_EXISTS_MSG,
    TABLE_NOT_FOUND_MSG,
    VALID_TYPES,
)


def format_columns(schema):
    """Возвращает схему таблицы строкой вида "ID:int, name:str"."""
    return ", ".join(
        f"{name}{COLUMN_SEPARATOR}{col_type}" for name, col_type in schema.items()
    )


def parse_column(column, schema):
    """Разбирает описание столбца "имя:тип"; при ошибке возвращает None."""
    name, separator, col_type = column.partition(COLUMN_SEPARATOR)
    is_valid = (
        separator
        and name.isidentifier()
        and name not in schema
        and col_type in VALID_TYPES
    )
    return (name, col_type) if is_valid else None


def create_table(metadata, table_name, columns):
    """Создает таблицу со столбцом ID:int и столбцами columns."""
    if table_name in metadata:
        print(TABLE_EXISTS_MSG.format(table_name))
        return None
    if not table_name.isidentifier():
        print(INVALID_VALUE_MSG.format(table_name))
        return None

    schema = {ID_COLUMN: ID_TYPE}
    for column in columns:
        parsed = parse_column(column, schema)
        if parsed is None:
            print(INVALID_VALUE_MSG.format(column))
            return None
        name, col_type = parsed
        schema[name] = col_type

    metadata[table_name] = schema
    print(TABLE_CREATED_MSG.format(table_name, format_columns(schema)))
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(TABLE_NOT_FOUND_MSG.format(table_name))
        return None

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
