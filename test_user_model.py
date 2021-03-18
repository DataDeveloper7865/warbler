"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
# from env import USER_POSTGRES, PASSWORD_POSTGRES

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# mac config
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

#windows config
# os.environ['DATABASE_URL'] = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@127.0.0.1/warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.u1 = User(
            email="test@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url=None
        )

        self.u2 = User(
            email="test123@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        self.u1.followers.append(self.u2)

        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 1)
        self.assertIsInstance(self.__repr__(), str)
        self.assertEqual(self.u2.is_following(self.u1), True)
        self.assertEqual(self.u1.is_following(self.u2), False)
        self.assertEqual(self.u2.is_followed_by(self.u1), False)
        self.assertEqual(self.u1.is_followed_by(self.u2), True)
        self.assertIsInstance(User.signup( 
                                self.u1.username, 
                                self.u1.email, 
                                self.u1.password,
                                self.u1.image_url), User)
        # self.assertEqual(User.signup( 
        #                         self.u1.username, 
        #                         self.u1.email, 
        #                         self.u1.image_url), "Invalid Num params")


    def test_signup_Func(self):
        invalid_user = User.signup(
            username="User3",
            email="123@gmail.com",
            password="pass",
            image_url=None
        )

        invalid_user.assertRaises(TypeError)