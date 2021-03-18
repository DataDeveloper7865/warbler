"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from sqlalchemy import exc

from models import db, User, Message, Follows
from env import USER_POSTGRES, PASSWORD_POSTGRES

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# mac config
# os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# windows config
os.environ['DATABASE_URL'] = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@127.0.0.1/warbler_test"

# Now we can import app


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

        self.u1 = User.signup(
            email="test@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url=None
        )

        self.u1.id = 9999

        self.u2 = User.signup(
            email="test123@test.com",
            username="testuser2",
            password="HASHED_PASSWORD123",
            image_url=None
        )

        self.u2.id = 10000

        self.m1 = Message(
            text = "blah blah blah",
            user_id = self.u1.id
        )

        db.session.add(self.m1, self.u1)
        db.session.commit()

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result

    def test_message_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        # 1 Does the repr method work as expected?
        self.assertEqual(len(self.u1.messages), 1)
        self.assertEqual(self.u1.messages[0].text, "blah blah blah")
        self.assertIsInstance(self.m1, Message)

    def test_message_likes_relationship(self):

        self.m2 = Message(
            text = "blah2 blah2 blah2",
            user_id = self.u1.id
        )

        self.u2.liked_messages.append(self.m2)

        self.assertIn(self.m2, self.u2.liked_messages)
        self.assertNotIn(self.m1, self.u2.liked_messages)