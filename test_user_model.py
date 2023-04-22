"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        

       

        db.session.add(u)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        follow = Follows(
            user_being_followed_id = u1.id,
            user_following_id = u2.id
        )

        db.session.add(follow)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(str(u), f"<User #{u.id}: {u.username}, {u.email}>")
        self.assertEqual(u1.is_followed_by(u2), 1)
        self.assertEqual(u2.is_followed_by(u1), 0)
        self.assertEqual(u1.is_following(u2), 0)
        self.assertEqual(u2.is_following(u1), 1)
        self.assertIn("testuser3, test3@test.de",str(User.signup("testuser3", "test3@test.de", "Bird", "https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453__340.jpg")))
        self.assertIn("testuser3, test3@test.de", str(User.authenticate("testuser3", "Bird")))
        self.assertEquals(False, User.authenticate("testuser3", "Birdyyy"))
        self.assertEquals(False, User.authenticate("testuser5", "Bird"))