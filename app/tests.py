import unittest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from app.models import User
@unittest.skip("Priority 1")
class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            "name": "TestUser",
            "age": 25,
            "password": "testpassword",
            "interests": {"coding": 80, "gaming": 70}
        }
        response = self.client.post('/api/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

@unittest.skip("Priority 2")
class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(name="TestUser", age=25, password="testpassword", interests={
                 "cooking": 21,
                 "computers": 66,
                 "cars": 53
             })

    def test_user_login(self):
        data = {
            "name": "TestUser",
            "password": "testpassword"
        }
        response = self.client.post('/api/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

@unittest.skip("Priority 3")
class OnlineUserListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(name="User1", age=30, password="test1", interests= {
                 "cooking": 21,
                 "computers": 66,
                 "cars": 53
             })
        self.user2 = User.objects.create_user(name="User2", age=25, password="test2", interests= {
                 "cooking": 51,
                 "computers": 26,
                 "cars": 63
             })

    def test_online_user_list(self):
        response = self.client.get('/api/online-users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(len(response.data)), True) 


