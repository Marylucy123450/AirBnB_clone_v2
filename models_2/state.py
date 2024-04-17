#!/usr/bin/python3
"""This module defines the State class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel, Base):
    """A class for representing State objects"""
    if models.storage_type == "db":
        __tablename__ = 'states'

        name = Column(String(128), nullable=False)

        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_type != "db":
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances"""
            all_cities = models.storage.all(City).values()
            return [city for city in all_cities
                    if city.state_id == self.id]
