#!/usr/bin/python3
""" Review module for the HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """This class represents a review in the application."""
    __tablename__ = 'reviews'

    place_id = Column(String(60),
                      ForeignKey('places.id', ondelete='CASCADE'),
                      nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    text = Column(String(1024), nullable=False)
