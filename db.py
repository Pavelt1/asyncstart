import os

from sqlalchemy import MetaData, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER',"postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',"0596")
POSTGRES_DB = os.getenv('POSTGRES_DB',"postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","5432")

DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_HOST}/{POSTGRES_DB}"
engine = create_async_engine(DSN,echo=True) #Указание echo=True при инициализации движка позволит нам увидеть сгенерированные SQL-запросы в консоли.

Base = declarative_base(metadata=MetaData())

# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class People(Base):
    __tablename__ = "people"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    birth_year:Mapped[int] = mapped_column(Integer)
    eye_color:Mapped[str] = mapped_column(String)
    films:Mapped[str] = mapped_column(String)#строка с названиями фильмов через запятую
    gender:Mapped[str] = mapped_column(String)
    hair_color:Mapped[str] = mapped_column(String)
    height:Mapped[int] = mapped_column(Integer)
    homeworld:Mapped[str] = mapped_column(String)
    mass:Mapped[int] = mapped_column(Integer)
    name:Mapped[str] = mapped_column(String)
    skin_color:Mapped[str] = mapped_column(String)
    species:Mapped[str] = mapped_column(String) #строка с названиями типов через запятую
    starships:Mapped[str] = mapped_column(String) #строка с названиями кораблей через запятую
    vehicles:Mapped[str] = mapped_column(String) #строка с названиями транспорта через запятую
    

    def dict(self):
        return{
            "id":self.id,
            "name":self.name
            }


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

list_for_orm = ["birth_year","eye_color","films","gender",
                "hair_color","height","homeworld","mass","name",
                "skin_color","species","starships","vehicles"]
