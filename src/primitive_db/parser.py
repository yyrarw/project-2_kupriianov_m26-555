"""Разбор сложных команд: значения для insert, условия where и set."""

import shlex

from primitive_db.constants import (
    ASSIGN_SIGN,
    BOOL_LITERALS,
    CLOSE_PAREN,
    INVALID_VALUE_MSG,
    KEYWORD_AND,
    KEYWORD_FROM,
    KEYWORD_INTO,
    KEYWORD_SET,
    KEYWORD_VALUES,
    KEYWORD_WHERE,
    OPEN_PAREN,
    PUNCTUATION_CHARS,
    QUOTE_CHARS,
    VALUES_SEPARATOR,
)


def invalid(value):
    """Создает исключение о некорректном значении."""
    return ValueError(INVALID_VALUE_MSG.format(value))


def tokenize(text):
    """Разбивает текст на токены; строки в кавычках остаются одним токеном."""
    lexer = shlex.shlex(text, posix=False, punctuation_chars=PUNCTUATION_CHARS)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        raise invalid(text) from None


def is_keyword(token, keyword):
    """Проверяет, что токен является ключевым словом (без учета регистра)."""
    return token.lower() == keyword


def find_keyword(tokens, keyword):
    """Возвращает позицию ключевого слова в списке токенов или -1."""
    for index, token in enumerate(tokens):
        if is_keyword(token, keyword):
            return index
    return -1


def parse_value(token):
    """Превращает токен в значение: "строка" -> str, true/false -> bool, 28 -> int."""
    if len(token) >= 2 and token[0] in QUOTE_CHARS and token[-1] == token[0]:
        return token[1:-1]
    if token.lower() in BOOL_LITERALS:
        return BOOL_LITERALS[token.lower()]
    try:
        return int(token)
    except ValueError:
        raise invalid(token) from None


def split_by(tokens, separator):
    """Делит список токенов на части по токену-разделителю."""
    parts = [[]]
    for token in tokens:
        if is_keyword(token, separator):
            parts.append([])
        else:
            parts[-1].append(token)
    return parts


def parse_assignments(tokens, separator, text):
    """Разбирает "столбец = значение" через separator в словарь."""
    result = {}
    for part in split_by(tokens, separator):
        if len(part) != 3 or part[1] != ASSIGN_SIGN or not part[0].isidentifier():
            raise invalid(" ".join(part) or text)
        column, _, value = part
        if column in result:
            raise invalid(column)
        result[column] = parse_value(value)
    return result


def parse_where(tokens, text):
    """Разбирает условие where: "age = 28 and name = "Ann"" -> словарь."""
    return parse_assignments(tokens, KEYWORD_AND, text)


def parse_set(tokens, text):
    """Разбирает часть set: "age = 29, name = "Ann"" -> словарь."""
    return parse_assignments(tokens, VALUES_SEPARATOR, text)


def parse_values(tokens, text):
    """Разбирает список значений в скобках: ( "Ann" , 28 ) -> ["Ann", 28]."""
    if len(tokens) < 3 or tokens[0] != OPEN_PAREN or tokens[-1] != CLOSE_PAREN:
        raise invalid(text)
    values = []
    for part in split_by(tokens[1:-1], VALUES_SEPARATOR):
        if len(part) != 1:
            raise invalid(" ".join(part) or text)
        values.append(parse_value(part[0]))
    return values


def expect_keyword(tokens, index, keyword, text):
    """Проверяет, что на позиции index стоит нужное ключевое слово."""
    if index >= len(tokens) or not is_keyword(tokens[index], keyword):
        raise invalid(text)


def parse_insert(text):
    """Разбирает "into <таблица> values (...)" -> (таблица, значения)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 0, KEYWORD_INTO, text)
    expect_keyword(tokens, 2, KEYWORD_VALUES, text)
    return tokens[1], parse_values(tokens[3:], text)


def parse_select(text):
    """Разбирает "from <таблица> [where ...]" -> (таблица, условие или None)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 0, KEYWORD_FROM, text)
    if len(tokens) < 2:
        raise invalid(text)
    if len(tokens) == 2:
        return tokens[1], None
    expect_keyword(tokens, 2, KEYWORD_WHERE, text)
    return tokens[1], parse_where(tokens[3:], text)


def parse_update(text):
    """Разбирает "<таблица> set ... where ..." -> (таблица, set, where)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 1, KEYWORD_SET, text)
    where_index = find_keyword(tokens, KEYWORD_WHERE)
    if where_index == -1:
        raise invalid(text)
    set_clause = parse_set(tokens[2:where_index], text)
    return tokens[0], set_clause, parse_where(tokens[where_index + 1 :], text)


def parse_delete(text):
    """Разбирает "from <таблица> where ..." -> (таблица, условие)."""
    tokens = tokenize(text)
    expect_keyword(tokens, 0, KEYWORD_FROM, text)
    expect_keyword(tokens, 2, KEYWORD_WHERE, text)
    return tokens[1], parse_where(tokens[3:], text)
