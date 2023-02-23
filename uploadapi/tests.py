from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account, AccountTier


class ImageTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test123', password='asdf4444')
        self.acc_tier = AccountTier.objects.create(name='Enterprise', has_image_link=True, has_expiring_links=True)
        self.acc = Account.objects.create(user=self.user, account_tier=self.acc_tier)
        self.client.force_login(user=self.user)


    def test_upload_image(self):
        file = open('web3.jpg', 'rb')
        data = {
            'account': self.acc,
            'image': file
        }
        response = self.client.post(reverse('uploadapi:images-list'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_fail_upload_textfile(self):
        file = open('test.txt', 'rb')
        data = {
            'account': self.acc,
            'image': file
        }
        response = self.client.post(reverse('uploadapi:images-list'), data, format='multipart')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_images(self):
        response = self.client.get(reverse('uploadapi:images-list'), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



