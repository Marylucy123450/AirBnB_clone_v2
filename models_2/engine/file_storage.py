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

classes = {"BaseModel": BaseModel, "Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


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

        new_dict = {}
        for key, dict in self.__objects.items():
            # comparing cls with both class object and class name (as string)
            if cls == dict.__class__ or cls == dict.__class__.__name__:
                new_dict[key] = dict
        return new_dict


    def new(self, obj):
        """
        creates a new object and saves it to __objects
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj


    def save(self):
        """
        update the JSON file to reflect any change in the objects
        """
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="UTF-8") as json_file:
            json.dump(json_objects, json_file)


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
                obj_instance = classes[dict["__class__"]](**dict)
                self.__objects[id] = obj_instance


    def delete(self, obj=None):
        """
        Deletes an object from __objects if it exists.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]


    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
