"""Декораторы для операций с базой данных и замыкание для кэширования."""

import time

import prompt

from primitive_db.constants import (
    ACTION_CANCELLED_MSG,
    CONFIRM_PROMPT,
    CONFIRM_YES,
    FILE_NOT_FOUND_MSG,
    LOG_TIME_MSG,
    UNEXPECTED_ERROR_MSG,
)


def copy_metadata(wrapper, func):
    """Переносит имя и docstring исходной функции на обертку."""
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_db_errors(func):
    """Перехватывает ошибки операции, печатает сообщение и возвращает None."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(FILE_NOT_FOUND_MSG)
        except (KeyError, ValueError) as error:
            print(error.args[0] if error.args else error)
        except Exception as error:
            print(UNEXPECTED_ERROR_MSG.format(error))
        return None

    return copy_metadata(wrapper, func)


def ask_confirmation(action_name):
    """Спрашивает подтверждение; Ctrl+D или Ctrl+C считаются отказом."""
    try:
        answer = prompt.string(CONFIRM_PROMPT.format(action_name))
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer.strip().lower() == CONFIRM_YES


def confirm_action(action_name):
    """Фабрика декораторов: перед действием запрашивает подтверждение [y/n]."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not ask_confirmation(action_name):
                print(ACTION_CANCELLED_MSG)
                return None
            return func(*args, **kwargs)

        return copy_metadata(wrapper, func)

    return decorator


def log_time(func):
    """Замеряет время выполнения функции и печатает его."""

    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(LOG_TIME_MSG.format(func.__name__, elapsed))
        return result

    return copy_metadata(wrapper, func)
