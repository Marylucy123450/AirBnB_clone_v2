#!/usr/bin/python3
"""This module defines the Place class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from models.amenity import Amenity
from models.review import Review
import os

metadata = Base.metadata

place_amenity = Table('place_amenity',
                      metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id', ondelete='CASCADE')
                             ),
                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id', ondelete='CASCADE')
                             )
                        )


class Place(BaseModel, Base):
    """This class represents a place in the application."""
    __tablename__ = 'places'

    city_id = Column(String(60),
                    ForeignKey('cities.id', ondelete='CASCADE'),
                    nullable=False)
    user_id = Column(String(60),
                    ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place',
                                cascade='all, delete-orphan',
                                passive_deletes=True)

        amenities = relationship('Amenity', backref='place_amenities',
                                    cascade='all, delete',
                                    secondary=place_amenity,
                                    viewonly=False,
                                    passive_deletes=True)

    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Getter function for reviews attribute"""
            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Getter attribute to return the list of Amenity instances."""
            all_amenities = models.storage.all(Amenity).values()
            return [amenity for amenity in all_amenities
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter method for amenities."""
            if not isinstance(obj, Amenity):
                return
            self.amenity_ids.append(obj.id)
