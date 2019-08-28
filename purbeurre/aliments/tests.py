from django.test import TestCase
from django.contrib.auth.models import User
from .models import Aliment


class AlimentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@free.fr', password='testhello')
        user_1 = User.objects.create_user(username='anothertest', email='anothertest@free.fr', password='anothertesthello')
        Aliment.objects.create(user=user, name="chevre chaud")
        Aliment.objects.create(user=user_1, name="chevre chaud")

    def test_get_aliment(self):
        users = User.objects.filter(aliment__name="chevre chaud")
        self.assertEqual(users.first().username, "test")
        self.assertEqual(users.last().username, "anothertest")
