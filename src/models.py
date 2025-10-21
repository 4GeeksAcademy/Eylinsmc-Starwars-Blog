from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(15), nullable=True)
    lastname: Mapped[str] = mapped_column(String(15), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    favorite_planets = relationship("Favorite_Planet", back_populates="user", cascade="all, delete-orphan")
    favorite_characters = relationship("Favorite_Character", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    population: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    fav_planet = relationship("Favorite_Planet", back_populates="planet")


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    fav_character = relationship("Favorite_Character", back_populates="character")


class Favorite_Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="fav_planet")


class Favorite_Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="fav_character")
