#!/usr/bin/env python3
"""
This a simple storage engine that serializes instances to a
JSON file and deserializes JSON file to instances.
"""
import json


class FileStorage:
    """
    `FileStorage` uses JSON to serialize and deserializes
    object instances, while also handling saving to an
    abstract storage file.
    + ``__file_path``: string - path to the JSON file (ex: file.json)
    + ``__objects``: dictionary - empty but will store all objects
      by ``<class name>.id``.
    """
    __file_path = "file.json"
    __objects = {}

    # The Public instance methods
    def all(self):
        """ Return the dictionary ``__objects``"""
        return FileStorage.__objects

    def new(self, obj):
        """To Sets in ``__objects`` the ``obj`` with key
        ``<obj class name>.id``"""
        from models.base_model import BaseModel
        if obj and isinstance(obj, BaseModel):
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects.update({key: obj})

    def save(self):
        """To Serializes ``__objects`` to the JSON file ``__file_path``."""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fi:
            objs = {}
            for key, obj in FileStorage.__objects.items():
                objs.update({key: obj.to_dict()})
            json.dump(objs, fi)

    def reload(self):
        """To deserializes the JSON file to ``__objects`` only if
        ``__file_path`` exists, otherwise; do nothing and no
        exception should be raised."""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as fi:

                # Files import statements
                from models.base_model import BaseModel
                from models.user import User
                from models.state import State
                from models.city import City
                from models.amenity import Amenity
                from models.place import Place
                from models.review import Review

                objs = json.loads(fi.read())
                FileStorage.__objects = {}
                for key, obj in objs.items():
                    _class = obj["__class__"]
                    _obj = eval("{}({})".format(_class, "**obj"))
                    self.new(_obj)

        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
