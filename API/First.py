import asyncio


async def get_data():
    await asyncio.sleep(2)

    return "Data received"


async def main():
    result = await get_data()

    print(result)


if __name__ == "__main__":
    asyncio.run(main())













    