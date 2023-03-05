from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from database.database import Base, db

db.init()


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    __tablename__ = 'tablename'

    @classmethod
    async def create(cls, **kwargs):
        object = cls(**kwargs)
        db.add(object)
        try:
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

    author = relationship('Theme', back_populates='theme')

    def __repr__(self):
        return self.first_name + ' ' + self.last_name


class Theme(CreatedModel):
    __tablename__ = 'themes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    author_id = Column(Integer, ForeignKey('users.id'))

    theme = relationship('User', back_populates='author')

# class Test(CreatedModel):
#     id = Column(Integer, autoincrement=True, primary_key=True)
#
#     pass
