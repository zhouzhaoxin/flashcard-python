from sqlalchemy import String, Text, Integer, SmallInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper

from config import conf

engine = create_engine(conf.DATABASE.SCHEMA)
session = sessionmaker(bind=engine)
session = scoped_session(session)
Base = declarative_base()


class BaseMixin:

    @staticmethod
    def model2dict(model):
        if not model:
            return {}
        return {col: getattr(model, col) for col in model.fields}

    @property
    def fields(self):
        return class_mapper(self.__class__).columns.keys()

    def add(self):
        if self.id and int(self.id) < 0:
            self.id = None
        session.add(self)
        session.commit()

    def update(self):
        obj = session.query(self.__class__).filter_by(id=self.id).one()
        for field in self.fields[1:]:
            update_object = getattr(self, field)
            if update_object:
                setattr(obj, field, update_object)
        session.commit()

    def delete(self):
        card = session.query(self.__class__).filter_by(id=self.id).one()
        session.delete(card)
        session.commit()

    def query(self, page=None, size=None):
        q = session.query(self.__class__)
        for field in self.fields:
            query_obj = getattr(self, field)
            query_cls = getattr(self.__class__, field)
            if field == 'id' and query_obj == -1:
                continue
            if query_obj:
                if type(query_cls.type) in (Integer, SmallInteger):
                    q = q.filter(getattr(self.__class__, field) == query_obj)
                elif type(query_cls.type) in (Text, String):
                    q = q.filter(getattr(self.__class__, field).like("%{}%".format(query_obj)))
        q = q.order_by(self.__class__.id.desc())
        if page and size:
            page = (page - 1) * size
            q = q.offset(page).limit(size)
        res = q.all()
        return [self.model2dict(r) for r in res], len(res)

    def explict_query(self, page=None, size=None):
        q = session.query(self.__class__)
        for field in self.fields:
            query_obj = getattr(self, field)
            if field == 'id' and query_obj == -1:
                continue
            if query_obj:
                q = q.filter(getattr(self.__class__, field) == query_obj)
        q = q.order_by(self.__class__.id.desc())
        if page and size:
            page = (page - 1) * size
            q = q.offset(page).limit(size)
        print(q)
        res = q.all()
        return [self.model2dict(r) for r in res], len(res)
