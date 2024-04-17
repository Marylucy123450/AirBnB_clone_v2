#!/usr/bin/python3
"""This module defines the Amenity class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """This class represents an amenity in the application."""
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
