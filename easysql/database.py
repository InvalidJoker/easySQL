from .types import SearchType
from .convertor import conv_vals, split_vals, format_string
from .connector import Connector


class EasyDatabase(Connector):
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name

        super().__init__(self.db_name)

    async def __id_checker__(self, table_name: str):
        return await self.select(
            f"SELECT id FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})",
            "one",
        )

    async def create_table(
        self,
        table_name: str,
        columns: dict,
        check_if_exists: bool = True,
        defaults: dict = None,
    ) -> None:
        """Create a table in the database"""
        columns = split_vals(columns)
        columns = conv_vals(columns, defaults)

        if check_if_exists:
            exi_str = "CREATE TABLE IF NOT EXISTS"
        else:
            exi_str = "CREATE TABLE"

        await self.execute(f"{exi_str} {table_name} ({columns})")

    async def get(
        self,
        table_name: str,
        data: list,
        where: dict = None,
        type: SearchType = SearchType.ALL,
    ) -> list:
        """Get data from the database"""
        data_len = len(data)
        data_string: str = ""
        args_tuple: tuple = ()

        for index, item in enumerate(data):
            data_string += format_string(f"{item}", index, data_len)

        if where is None:
            return await self.select(f"SELECT {data_string} FROM {table_name}", type)

        splied = split_vals(where)
        find_string = ""

        for key, _ in where.items():
            find_string += f"{key} = ? AND "

        find_string = find_string[:-5]

        args_tuple: tuple = ()
        for x in splied:
            args_tuple += (x[1],)

        return await self.select(
            f"SELECT {data_string} FROM {table_name} WHERE {find_string}",
            type,
            args_tuple,
        )

    async def remove(
        self, table_name: str, data: list = None, where: dict = None
    ) -> None:
        """Remove data from the database"""
        if data is None and where is None:
            await self.execute(f"DELETE FROM {table_name}")
            return

        elif data is None and where is not None:
            splied = split_vals(where)
            find_string = ""

            for key, _ in where.items():
                find_string += f"{key} = ? AND "

            find_string = find_string[:-5]

            args_tuple: tuple = ()
            for x in splied:
                args_tuple += (x[1],)
            await self.execute(
                f"DELETE FROM {table_name} WHERE {find_string}", args_tuple
            )
            return

        data_len = len(data)
        data_string: str = ""
        args_tuple: tuple = ()

        for index, item in enumerate(data):
            data_string += format_string(f"{item}", index, data_len)

        if where is None:
            for key in data:
                await self.execute(f"UPDATE {table_name} SET {key} = NULL")
            return

        splied = split_vals(where)
        find_string = ""

        for key, _ in where.items():
            find_string += f"{key} = ? AND "

        find_string = find_string[:-5]

        args_tuple: tuple = ()
        for x in splied:
            args_tuple += (x[1],)

        for key in data:
            await self.execute(
                f"UPDATE {table_name} SET {key} = NULL WHERE {find_string}", args_tuple
            )

    async def update(self, table_name: str, data: dict, where: dict = None) -> None:
        """Update data in the database"""
        data_va = split_vals(data)
        data_len = len(data)
        data_string: str = ""
        args_tuple: tuple = ()

        for index, item in enumerate(data):
            data_string += format_string(f"{item} = ?", index, data_len)

        for x in data_va:
            args_tuple += (x[1],)

        if where is None:
            return await self.execute(
                f"UPDATE {table_name} SET {data_string}", args_tuple
            )

        splied = split_vals(where)
        find_string = ""

        for key, _ in where.items():
            find_string += f"{key} = ? AND "

        find_string = find_string[:-5]

        for x in splied:
            args_tuple += (x[1],)

        return await self.execute(
            f"UPDATE {table_name} SET {data_string} WHERE {find_string}", args_tuple
        )

    async def add(self, table_name: str, input: dict) -> None:
        """Add data to the database"""
        data = split_vals(input)
        sql_string: str = ""
        for key, _ in input.items():
            sql_string += f"{key}, "

        sql_string = sql_string[:-2]

        data_len = len(data)
        id = await self.__id_checker__(table_name)

        if id is None:
            id = 0

        else:
            id = id[0] + 1

        data_string: str = ""
        args_tuple: tuple = ()

        question_marks = ", ".join(["?"] * (data_len))
        for x in data:
            args_tuple += (x[1],)
        for index, item in enumerate(data):
            data_string += format_string(f"{item[1]}", index, data_len)

        await self.execute(
            f"INSERT INTO {table_name}({sql_string}) VALUES ({question_marks})",
            args_tuple,
        )
