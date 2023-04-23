"""User View tests."""


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()



app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for Users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()


    def test_user_signup(self):
        """Can we sign up a user?"""


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/signup", data={"username": "Testuser2", "password": "passIT", "email": "testuser2@test.de"})
            
        
            # Test response status code
            self.assertEqual(resp.status_code, 302)
                
            #Test if right URL in redirect
            self.assertIn('href="/"', str(resp.data))

            # Test if user in Database
            self.assertIn("Testuser2", str(User.query.all()))

    def test_user_list(self):
        """Can we see user list?"""


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            u = self.testuser

            u2 = User(username = "testuser2",
                      email= "testuser2@gmx.de",
                      password="testuser2")
            
            db.session.add(u2)
            db.session.commit()

            resp = c.get("/users")
            
        
            # Test response status code
            self.assertEqual(resp.status_code, 200)
                
            #Test if both created users in HTML response
            self.assertIn('"Image for testuser"', str(resp.data))
            self.assertIn('"Image for testuser2"', str(resp.data))


    def test_user_show(self):
        """Can we see user details?"""


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            u = self.testuser


            resp = c.get(f"/users/{u.id}")
            
        
            # Test response status code
            self.assertEqual(resp.status_code, 200)
                
            #Test if testuser in HTML response
            self.assertIn(f'<img src="{ u.image_url }" alt="Image for {u.username }" id="profile-avatar">', str(resp.data))

    

    def test_add_follow(self):
        """Can we add follows?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            u = self.testuser
            utb = User(username = "followme",
                       email = "follow@follow.de",
                       password = "Followme")
            db.session.add(utb)
            db.session.commit()
            
            resp = c.post(f"/users/follow/{utb.id}")

            self.assertEqual(resp.status_code, 302)
            self.assertIn(f"users/{u.id}/following", str(resp.data))

    def test_add_follow_loggedout(self):
        """Can we add follows?"""
        with self.client as c:
            
            u = self.testuser
            utb = User(username = "followme",
                       email = "follow@follow.de",
                       password = "Followme")
            db.session.add(utb)
            db.session.commit()

            
            resp = c.post(f"/users/follow/{utb.id}")

            self.assertEqual(resp.status_code, 302)
            self.assertIn('<p>You should be redirected automatically to target URL: <a href="/">/</a>', str(resp.data))



    def test_show_following_loggedin(self):
        """Can we see following users?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            u = self.testuser
            utb = User(username = "followme",
                       email = "follow@follow.de",
                       password = "Followme")
            db.session.add(utb)
            db.session.commit()

            f = Follows(user_being_followed_id = utb.id, user_following_id = u.id)
            
            db.session.add(f)
            db.session.commit()

            resp = c.get(f"/users/{u.id}/following")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{utb.username}", str(resp.data))

    

    def test_show_following_loggedout(self):
        """Can we see following users?"""
        with self.client as c:
            

            u = self.testuser
            utb = User(username = "followme",
                       email = "follow@follow.de",
                       password = "Followme")
            db.session.add(utb)
            db.session.commit()

            f = Follows(user_being_followed_id = utb.id, user_following_id = u.id)
            
            db.session.add(f)
            db.session.commit()

            resp = c.get(f"/users/{u.id}/following")

            self.assertEqual(resp.status_code, 302)
            self.assertIn('target URL: <a href="/">/</a>', str(resp.data))

  





            

