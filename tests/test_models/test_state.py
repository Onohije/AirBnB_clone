#!/usr/bin/env python3
"""
A unit test module for testing ``models/state.py`` module.
"""

import unittest
from models.state import State
from datetime import datetime


class Test_State(unittest.TestCase):
    """
    Test the fundamental features of the State class.
    """

    def test_instance_uuid_is_unique(self):
        """
        This test method validates that the behavior aligns
        precisely with its method name.
        """
        user1 = State()
        user2 = State()
        self.assertNotEqual(user1.id, user2.id)

    def test_instance_created_at_is_str(self):
        """
        This method of this test class tests for precisely
        what the name of the method reads.
        """
        user1 = State()
        self.assertEqual(type(user1.created_at), datetime)
        self.assertEqual(type(user1.updated_at), datetime)

    def test_save_method(self):
        """
        This method of this test class tests for precisely
        what the name of the method reads.
        """
        from time import sleep
        user1 = State()
        sleep(2)
        user1.save()
        self.assertNotEqual(user1.created_at, user1.updated_at)

    def test_string_representation(self):
        """
        This method of this test class tests for precisely
        what the name of the method reads.
        """
        user1 = State()
        string = "[{}] ({}) {}".format(user1.__class__.__name__,
                                       user1.id, user1.__dict__)
        self.assertEqual(user1.__str__(), string)

    def test_instance_dictionary(self):
        """
        This method of this test class tests for precisely
        what the name of the method reads.
        """
        user1 = State()
        user1.name = "New Instance variable"
        self.assertTrue("__class__" in user1.to_dict())
        self.assertTrue("name" in user1.to_dict())

    def test_new_instance_from_dictionary(self):
        """
        This method of this test class tests for precisely
        what the name of the method reads.
        """
        user1 = State()
        model_json = user1.to_dict()
        user2 = State(**model_json)
        self.assertFalse(user1 is user2)

    def test_new_instance_datetime_variables(self):
        """
        This test method verifies that the behavior aligns
        precisely with its method name.
        """
        user1 = State()
        model_json = user1.to_dict()
        user2 = State(**model_json)
        self.assertEqual(type(user2.created_at), datetime)
        self.assertEqual(type(user2.updated_at), datetime)

    def test_new_instance_properties_against_old(self):
        """
        This test method confirms that the behavior aligns
        precisely with its method name.
        """
        user1 = State()
        user1.name = "New_Instance"
        model_json = user1.to_dict()
        user2 = State(**model_json)
        self.assertEqual(type(user1), type(user2))
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user1.name, user2.name)
