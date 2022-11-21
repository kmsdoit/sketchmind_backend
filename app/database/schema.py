from dataclasses import asdict

from fastapi import FastAPI
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship

from app.common.config import conf
from app.database.conn import Base, db


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))

        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()

        return obj

    @classmethod
    def get(cls,session: Session = None,**kwargs):
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key,val in kwargs.items():
            col = getattr(cls,key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("이미 가입된 계정이 있습니다")

        result = query.first()

        if not session:
            sess.close()

        return result


class Users(Base, BaseMixin):
    __tablename__ = "users"
    status = Column(Enum("active", "deleted", "blocked", name="activative_enum"), default="active")
    email = Column(String(length=255), nullable=True)
    pw = Column(String(length=2000), nullable=True)
    name = Column(String(length=255), nullable=True)
    phone_number = Column(String(length=20), nullable=True, unique=True)
    sns_type = Column(Enum("FB", "G", "K","N", name="social_enum"), nullable=True)
    marketing_agree = Column(Boolean, nullable=True, default=True)
    # keys = relationship("ApiKeys", back_populates="users")

class