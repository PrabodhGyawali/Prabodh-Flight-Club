from sqlalchemy import ForeignKey, Integer, String, JSON
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from typing import List



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class City(db.Model):
    __tablename__ = "iata"
    city_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    iata: Mapped[str] = mapped_column(String(3), unique=True)

class Users(db.Model):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column()
    # Children
    user_settings: Mapped[List["Settings"]] = relationship(back_populates="parent")

class Settings(db.Model):
    __tablename__ = "settings"
    setting_id: Mapped[int] = mapped_column(primary_key=True)
    city_price = mapped_column(JSON)
    arch_city_ptice = mapped_column(JSON)
    notification: Mapped[bool] = mapped_column()
    user_id = Mapped["Users"] = relationship(back_populates="user_settings") 

    


