from rest_framework.test import APITestCase
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token
from rest_framework import status
from src.cat import models


def create_user(email, name):
    user = FatUser.objects.create_user(
        username=name,
        password='password',
        email=email
    )
    return user


class CatTestCase(APITestCase):

    def setUp(self):
        self.user = create_user('zxczxczxczxxx', 'oaidoasdioasdois@mail.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_cat(self):
        cat = self.user.cat.first().id
        response = self.client.get(f'/api/v1/cat/{cat}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

