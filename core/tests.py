from django.test import TestCase
from django.urls import reverse
# Create your tests here.
from rest_framework.test import APITestCase


class UserApiTestCase(APITestCase):
    def test_get(self):
        url = reverse('users-list')
        return self.client(url)



