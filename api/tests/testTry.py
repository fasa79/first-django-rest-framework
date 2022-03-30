from urllib import response
from django.test import TestCase
from django.urls import reverse

class testTry(TestCase):
    fixtures = ['try.json']

    def testPrint(self):
        data = self.client.get(reverse('all-data'))
        print(data.data)