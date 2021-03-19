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

        self.u2 = User.signup(
            email="test123@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=None
        )

        self.u1.followers.append(self.u2)

        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        # 1 Does the repr method work as expected?
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 1)
        self.assertIsInstance(self.__repr__(), str)

    def test_is_following(self):
        # 2. Does is_following successfully detect when user1 is following user2?
        # 3. Does is_following successfully detect when user1 is not following user2?
        self.assertEqual(self.u2.is_following(self.u1), True)
        self.assertEqual(self.u1.is_following(self.u2), False)

    def test_is_followed_by(self):
        # 4. Does is_followed_by successfully detect when user1 is followed by user2?
        # 5. Does is_followed_by successfully detect when user1 is not followed by user2?
        self.assertEqual(self.u2.is_followed_by(self.u1), False)
        self.assertEqual(self.u1.is_followed_by(self.u2), True)

    def test_signup_succeeds(self):
        self.assertIsInstance(User.signup(
            self.u1.username,
            self.u1.email,
            self.u1.password,
            self.u1.image_url), User)

    def test_signup_fails(self):
        """Invallid email """
        User.signup("User3", None, "pass123", None)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_authenticate_successful(self):
        # 8. Does User.authenticate successfully return a user when given a valid username and password?

        u = User.authenticate(self.u1.username, "HASHED_PASSWORD")
        self.assertIsInstance(u, User)

    def test_authenticate_username(self):
        # 9. Does User.authenticate fail to return a user when the username is invalid?
        u = User.authenticate('garygarygary', self.u1.password)
        self.assertNotIsInstance(u, User)

    def test_authenticate_password(self):
        # 10. Does User.authenticate fail to return a user when the password is invalid?
        u = User.authenticate(self.u1.username, "WRONG_PASSWORD")
        self.assertNotIsInstance(u, User)
