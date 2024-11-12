import aiohttp
import asyncio
from db import init_models
from crud import format_data_for_ORM, safe_ORM


async def get_http(Url: str) -> dict:# Достает json из url
    async with aiohttp.ClientSession() as session:
        response = await session.get(Url)
        return await response.json()

async def main():
    await init_models()
    url = "https://swapi.dev/api/people/"
    result = []
    len_list_people = (((await get_http(url))["count"]) + 1)
    for i in range(1,(len_list_people + 1)):
        response = await get_http(f"{url}{i}/")
        result.append(safe_ORM(response))
    await asyncio.gather(*result)

if __name__ == "__main__":
    asyncio.run(main())