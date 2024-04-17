#!/usr/bin/python3
"""This module defines the City class"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """A class for representing City objects"""
    if models.storage_type == "db":
        __tablename__ = 'cities'

        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)

        places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    if models.storage_type != 'db':
        @property
        def places():
            """getter for list of places related to city"""
            place_list = []
            all_places = models.storage.all(Place)
            for place in all_places.values():
                if place_list.id == self.id:
                    place_list.append(place)
            return place_list
