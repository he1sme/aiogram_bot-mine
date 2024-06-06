from sqlalchemy import BigInteger, String, ForeignKey, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, selectinload
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind = engine, expire_on_commit = False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    money = mapped_column(BigInteger)


class CategoryPc(Base):
    __tablename__ = 'categories_pc'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Pc(Base):
    __tablename__ = 'pcs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column()
    mine: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

class CategoryCrypto(Base):
    __tablename__ = 'categories_crypto'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

class Crypto(Base):
    __tablename__ = 'crypto'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories_crypto.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, money=50))
            await session.commit()



async def get_categories_crypto(crypto_catigory_id):
    async with async_session() as session:
        return await session.scalars(select(Crypto).where(Crypto.category == crypto_catigory_id))
    

async def get_crypto(crypto_id):
    async with async_session() as session:
        return await session.scalar(select(Crypto).where(Crypto.id == crypto_id))


async def get_categories_all_crypto():
    async with async_session() as session:
        return await session.scalars(select(CategoryCrypto))


async def get_categories_all_pc():
    async with async_session() as session:
        return await session.scalars(select(CategoryPc))

async def update_crypto_price(crypto_id: int, new_price: int) -> None:
    async with async_session() as session:
        crypto = await session.get(Crypto, crypto_id)
        if crypto:
            crypto.price = new_price
            await session.commit()

async def get_category_pc(category_id):
    async with async_session() as session:
        return await session.scalar(select(Pc).where(Pc.category == category_id))


async def get_pc(pc_id):
    async with async_session() as session:
        return await session.scalar(select(Pc).where(Pc.id == pc_id))
        

async def create_user_table(tg_id: int) -> None:
    """Создает таблицу с названием tg_id пользователя"""
    async with engine.connect() as conn:
        # Создаем таблицу
        query = text(f"""
        CREATE TABLE IF NOT EXISTS table_{tg_id} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            amount INTEGER
        );
        """)
        await conn.execute(query)

        # Копируем данные из таблицы crypto

        query = text(f"""
        INSERT INTO table_{tg_id} (name)
        SELECT name
        FROM crypto;
        """)
        await conn.execute(query)