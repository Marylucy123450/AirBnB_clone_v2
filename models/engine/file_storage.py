#!/usr/bin/python3
"""
module containing FileStorage used for file storage
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


import os


class FileStorage:
    """
    serializes and deserializes instances to and from JSON file
    saved into file_path

    """

    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        """
        returns a dictionary containing every object
        """
        if cls is None:
            return self.__objects
        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """
        creates a new object and saves it to __objects
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        update the JSON file to reflect any change in the objects
        """
        temp = {}
        for key, obj in self.__objects.items():
            temp[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="UTF-8") as json_file:
            json.dump(temp, json_file)

    def reload(self):
        """
        update __objects dict to restore previously created objects
        """
        if not os.path.exists(self.__file_path):
            # Create an empty JSON file if it doesn't exist
            with open(self.__file_path, "w", encoding="UTF-8") as json_file:
                json.dump({}, json_file)

        with open(self.__file_path, "r", encoding="UTF-8") as json_file:
            data = json.load(json_file)
            for id, dict in data.items():
                obj_instance = eval(dict["__class__"])(**dict)
                self.__objects[id] = obj_instance

    def delete(self, obj=None):
        """
        Deletes an object from __objects if it exists.
        """
        if obj and obj.id in self.__objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
