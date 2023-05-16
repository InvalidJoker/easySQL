from enum import Enum


class Type(Enum):
    """Enum for the different types of data that can be stored in the database"""

    STRING = 1
    INTEGER = 2
    FLOAT = 3
    TIMESTAMP = 4

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Type):
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class SearchType:
    """Enum for the different types of searches that can be done in the database"""

    ALL = "all"
    ONE = "one"
