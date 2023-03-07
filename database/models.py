from datetime import datetime

from asyncpg import exceptions
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, TEXT, ARRAY
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from database.database import Base, db

db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    __tablename__ = 'tablename'

    @classmethod
    async def commit(cls):
        db.commit()

    @classmethod
    async def rollback(cls):
        db.rollback()

    @classmethod
    async def create(cls, commit=True, **kwargs):
        object = cls(**kwargs)
        db.add(object)
        try:
            if commit:
                await db.commit()
        except Exception:
            await db.rollback()
            raise
        return object

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def get(cls, id, **kwargs):
        query = select(cls).where(cls.id == id)
        objects = await db.execute(query)
        object = objects.first()[0]
        return object

    @classmethod
    async def get_all(cls, **kwargs):
        query = select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    # async def delete(cls, id):
    # query = sqlalchemy_delete(cls).where(cls.id == id)
    # await db.execute(query)
    # try:
    #     await db.commit()
    # except Exception:
    #     await db.rollback()
    #     raise
    # return True

    @classmethod
    async def counts(cls):
        objects_count_query = select(cls)
        objects_count = await db.execute(objects_count_query)
        return len(objects_count.scalars().all())


class CreatedModel(Base, AbstractClass):
    __abstract__ = True


class User(CreatedModel):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    lang = Column(String(5), default='en')
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    theme = relationship('Theme', back_populates='author')

    def __repr__(self):
        return self.first_name + ' ' + self.last_name



class Theme(CreatedModel):
    _status = {
        'MIX': 'MIX',
        'NOT MIX': 'NOT MIX',
        'QUESTIONS': 'QUESTIONS',
        'ANSWERS': 'ANSWERS'
    }

    __tablename__ = 'themes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    author_id = Column(String, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    status = Column(String)


    author = relationship('User', back_populates='theme')
    tests = relationship('Test', back_populates='theme')

    @classmethod
    async def create(cls, commit=True, **kwargs):
        print()
        return await super().create(commit, **kwargs)


class Test(CreatedModel):
    __tablename__ = 'tests'
    id = Column(Integer, autoincrement=True, primary_key=True)
    question = Column(TEXT)
    options = Column(ARRAY(String))
    answer = Column(Integer)
    theme_id = Column(Integer, ForeignKey('themes.id', ondelete='CASCADE'))

    theme = relationship('Theme', back_populates='tests')
