"""Константы приложения: пути к файлам, типы данных, тексты сообщений."""

# Файлы и директории
META_FILE = "db_meta.json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4

# Схема таблиц
ID_COLUMN = "ID"
ID_TYPE = "int"
VALID_TYPES = ("int", "str", "bool")
COLUMN_SEPARATOR = ":"

# Интерфейс
PROMPT_TEXT = ">>>Введите команду: "
COMMAND_EXIT = "exit"
COMMAND_HELP = "help"
COMMAND_CREATE_TABLE = "create_table"
COMMAND_DROP_TABLE = "drop_table"
COMMAND_LIST_TABLES = "list_tables"
KNOWN_COMMANDS = (
    COMMAND_EXIT,
    COMMAND_HELP,
    COMMAND_CREATE_TABLE,
    COMMAND_DROP_TABLE,
    COMMAND_LIST_TABLES,
)

# Сообщения
INVALID_VALUE_MSG = "Некорректное значение: {}. Попробуйте снова."
UNKNOWN_COMMAND_MSG = "Функции {} нет. Попробуйте снова."
TABLE_EXISTS_MSG = 'Ошибка: Таблица "{}" уже существует.'
TABLE_NOT_FOUND_MSG = 'Ошибка: Таблица "{}" не существует.'
TABLE_CREATED_MSG = 'Таблица "{}" успешно создана со столбцами: {}'
TABLE_DROPPED_MSG = 'Таблица "{}" успешно удалена.'
NO_TABLES_MSG = "В базе данных пока нет таблиц."
