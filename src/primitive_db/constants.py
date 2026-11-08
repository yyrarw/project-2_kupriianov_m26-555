"""Константы приложения: пути к файлам, типы данных, тексты сообщений."""

# Файлы и директории
META_FILE = "db_meta.json"
DATA_DIR = "data"
DATA_FILE_EXTENSION = ".json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4

# Схема таблиц
ID_COLUMN = "ID"
ID_TYPE = "int"
PYTHON_TYPES = {"int": int, "str": str, "bool": bool}
VALID_TYPES = tuple(PYTHON_TYPES)
COLUMN_SEPARATOR = ":"

# Интерфейс
PROMPT_TEXT = ">>>Введите команду: "
COMMAND_EXIT = "exit"
COMMAND_HELP = "help"
COMMAND_CREATE_TABLE = "create_table"
COMMAND_DROP_TABLE = "drop_table"
COMMAND_LIST_TABLES = "list_tables"
COMMAND_INSERT = "insert"
COMMAND_SELECT = "select"
COMMAND_UPDATE = "update"
COMMAND_DELETE = "delete"
COMMAND_INFO = "info"

# Сообщения
INVALID_VALUE_MSG = "Некорректное значение: {}. Попробуйте снова."
UNKNOWN_COMMAND_MSG = "Функции {} нет. Попробуйте снова."
TABLE_EXISTS_MSG = 'Ошибка: Таблица "{}" уже существует.'
TABLE_NOT_FOUND_MSG = 'Ошибка: Таблица "{}" не существует.'
TABLE_CREATED_MSG = 'Таблица "{}" успешно создана со столбцами: {}'
TABLE_DROPPED_MSG = 'Таблица "{}" успешно удалена.'
NO_TABLES_MSG = "В базе данных пока нет таблиц."
RECORD_INSERTED_MSG = 'Запись с ID={} успешно добавлена в таблицу "{}".'
RECORD_UPDATED_MSG = 'Запись с ID={} в таблице "{}" успешно обновлена.'
RECORD_DELETED_MSG = 'Запись с ID={} успешно удалена из таблицы "{}".'
NO_MATCHES_MSG = 'В таблице "{}" нет записей, подходящих под условие.'
NO_RECORDS_MSG = "Записи не найдены."
VALUES_COUNT_MSG = "ожидается значений: {}, передано: {}"
TABLE_INFO_MSG = "Таблица: {}\nСтолбцы: {}\nКоличество записей: {}"

# Синтаксис команд с данными
KEYWORD_INTO = "into"
KEYWORD_VALUES = "values"
KEYWORD_FROM = "from"
KEYWORD_WHERE = "where"
KEYWORD_SET = "set"
KEYWORD_AND = "and"
ASSIGN_SIGN = "="
VALUES_SEPARATOR = ","
OPEN_PAREN = "("
CLOSE_PAREN = ")"
PUNCTUATION_CHARS = ASSIGN_SIGN + VALUES_SEPARATOR + OPEN_PAREN + CLOSE_PAREN
QUOTE_CHARS = ('"', "'")
BOOL_LITERALS = {"true": True, "false": False}

# Декораторы
FILE_NOT_FOUND_MSG = (
    "Ошибка: Файл данных не найден. Возможно, база данных не инициализирована."
)
UNEXPECTED_ERROR_MSG = "Произошла непредвиденная ошибка: {}"
