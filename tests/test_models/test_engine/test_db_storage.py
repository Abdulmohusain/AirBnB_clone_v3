#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        state = State()
        state.name = "Lagos"
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(type(models.storage.all(State)), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        user = User()
        user.email = "abd@gmail.com"
        user.password = "qwerty"
        user.first_name = "julien"
        user.last_name = "Berber"
        models.storage.new(user)
        models.storage.save()
        self.assertEqual(len(models.storage.all()), 1)

        user2 = User()
        user2.email = "abd@gmail.com"
        user2.password = "qwerty"
        user2.first_name = "julien"
        user2.last_name = "Berber"
        models.storage.new(user2)
        models.storage.save()
        self.assertEqual(len(models.storage.all()), 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        user2 = User()
        user2.email = "abd@gmail.com"
        user2.password = "qwerty"
        user2.first_name = "julien"
        user2.last_name = "Berber"
        models.storage.new(user2)
        self.assertTrue(user2 in models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = State()
        state.name = "Lagos"
        models.storage.new(state)
        models.storage.save()
        self.assertTrue(state in models.storage.all(State).values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that retrieve one object:"""
        # Instance creation
        user = User()
        user_id = user.id
        user.email = "abd@gmail.com"
        user.password = "qwerty"
        user.first_name = "julien"
        user.last_name = "Berber"
        models.storage.new(user)

        user2 = User()
        user2.email = "abd@gmail.com"
        user2.password = "qwerty"
        user2.first_name = "julien"
        user2.last_name = "Berber"
        models.storage.new(user2)

        state = State()
        state.name = "Lagos"
        state_id = state.id
        models.storage.new(state)

        # save all models
        self.assertEqual(models.storage.get(User, user_id), user)
        self.assertNotEqual(models.storage.get(User, user_id), state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """method to count the number of objects in storage:"""
        user = User()
        user_id = user.id
        user.email = "abd@gmail.com"
        user.password = "qwerty"
        user.first_name = "julien"
        user.last_name = "Berber"
        models.storage.new(user)

        user2 = User()
        user2.email = "abd@gmail.com"
        user2.password = "qwerty"
        user2.first_name = "julien"
        user2.last_name = "Berber"
        models.storage.new(user2)

        state = State()
        state.name = "Lagos"
        state_id = state.id
        models.storage.new(state)

        # save all models
        models.storage.save()

        self.assertEqual(models.storage.count(), len(models.storage.all()))
        self.assertEqual(
            models.storage.count(State),
            len(models.storage.all(State))
        )
        self.assertEqual(
            models.storage.count(User),
            len(models.storage.all(User))
        )
