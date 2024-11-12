from db import People,async_session_maker,list_for_orm
from asynchttp import get_http



async def format_data_for_ORM(json_data: dict) -> dict: #собирает только те ключи которые нужны и списки url в одну строку c name  
    response = {}
    for i in list_for_orm:
        if json_data.get(i) and isinstance(json_data.get(i),list):
            name_attribute = []
            for o in json_data.get(i):
                data = await get_http(o)
                name = data.get("name")
                title = data.get("title")
                if name:
                    name_attribute.append(name)
                elif title:
                    name_attribute.append(title)
            response = {i : ", ".join(name_attribute)}
        else:
            response = {i : json_data[i]}
    return response



async def safe_ORM(data: dict) -> dict: #Добавляет в базу данных 
    async with async_session_maker() as session:
        valid_data = await format_data_for_ORM(data)
        new_people = People(**valid_data) 
        await session.add(new_people)
        await session.commit()
    return new_people