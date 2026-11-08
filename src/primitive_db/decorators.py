"""Декораторы для операций с базой данных и замыкание для кэширования."""

from primitive_db.constants import FILE_NOT_FOUND_MSG, UNEXPECTED_ERROR_MSG


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
