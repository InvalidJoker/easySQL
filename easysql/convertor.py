from typing import Union, List, Tuple

from .types import Type


def split_vals(dictionary: dict) -> List[Tuple[str, Union[str, int, float, bool]]]:
    """Split the values from the dictionary"""
    formatted = []

    for key in dictionary:
        formatted.append((key, dictionary[key]))

    return formatted


def conv_vals(values: list, defaults: dict = None) -> str:
    """Convert the values to a usable string"""
    end_string = "ID INTEGER PRIMARY KEY, "
    list_len = len(values)

    for index, value in enumerate(values):
        if value[1] is Type.STRING:
            if defaults is not None and value[0] in defaults:
                end_string += format_string(
                    f"{value[0]} TEXT DEFAULT '{defaults[value[0]]}'",
                    index,
                    list_len,
                )
            else:
                end_string += format_string(f"{value[0]} TEXT", index, list_len)

        elif value[1] is Type.INTEGER:
            if defaults is not None and value[0] in defaults:
                end_string += format_string(
                    f"{value[0]} INTEGER DEFAULT {defaults[value[0]]}",
                    index,
                    list_len,
                )

            else:
                end_string += format_string(f"{value[0]} INTEGER", index, list_len)

        elif value[1] is Type.FLOAT:
            if defaults is not None and value[0] in defaults:
                end_string += format_string(
                    f"{value[0]} FLOAT DEFAULT {defaults[value[0]]}",
                    index,
                    list_len,
                )
            else:
                end_string += format_string(f"{value[0]} FLOAT", index, list_len)

        elif value[1] is Type.TIMESTAMP:
            if defaults is not None and value[0] in defaults:
                end_string += format_string(
                    f"{value[0]} TIMESTAMP DEFAULT {defaults[value[0]]}",
                    index,
                    list_len,
                )
            else:
                end_string += format_string(f"{value[0]} TIMESTAMP", index, list_len)

        else:
            raise TypeError(f'Type "{value[1]}" is not supported')

    return end_string


def format_string(value, index, list_len):
    if index == list_len - 1:
        return f"{value}"
    else:
        return f"{value}, "
