import asyncio

from easysql import EasyDatabase, Type, SearchType


lazy = EasyDatabase("test.db")


async def main():
    await lazy.create_table(
        "test",
        {"name": Type.STRING, "age": Type.INTEGER},
    )

    await lazy.add(
        "test",
        {
            "name": "Tester",
            "age": 99,
        },
    )
    g1 = await lazy.get(
        "test",
        [
            "age",
        ],
        {
            "name": "Tester",
        },
        type=SearchType.ONE,
    )
    print(g1)
    g2 = await lazy.update(
        "test",
        {
            "name": "Tester",
        },
        {
            "age": 16,
        },
    )
    print(g2)
    await lazy.remove(
        "test",
        {
            "name": "Tester",
        },
    )


asyncio.run(main())
