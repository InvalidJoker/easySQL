import aiosqlite


class Connector:
    def __init__(self, path: str) -> None:
        self.path = path

    async def execute(self, code: str, args: tuple = None) -> None:
        if args is None:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(code)

                await db.commit()

        else:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(code, args)

                await db.commit()

    async def select(self, code: str, fetch: str, args: tuple = None):
        if args is None:
            async with aiosqlite.connect(self.path) as db:
                async with db.execute(code) as cursor:
                    if fetch == "one":
                        return await cursor.fetchone()

                    elif fetch == "all":
                        return await cursor.fetchall()

                    else:
                        raise ValueError(
                            f'the "fetch" argument must be "all" or "one" not {fetch}'
                        )

        else:
            async with aiosqlite.connect(self.path) as db:
                async with db.execute(code, args) as cursor:
                    if fetch == "one":
                        return await cursor.fetchone()

                    elif fetch == "all":
                        return await cursor.fetchall()

                    else:
                        raise ValueError(
                            f'the "fetch" argument must be "all" or "one" not {fetch}'
                        )
