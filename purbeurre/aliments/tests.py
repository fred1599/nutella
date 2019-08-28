from django.contrib.auth.models import User
from django.test import TestCase

from .models import Aliment


class AlimentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@free.fr', password='testhello')
        self.user_1 = User.objects.create_user(username='anothertest', email='anothertest@free.fr',
                                               password='anothertesthello')
        aliment = Aliment.objects.create(name="fromage")
        aliment = Aliment.objects.get(pk=aliment.pk)
        aliment.user_set.add(self.user_1, self.user)

    def test_get_user(self):
        users = User.objects.filter(aliment_set__name="fromage")
        self.assertEqual(users.first().username, 'test')
        self.assertEqual(users.last().username, 'anothertest')
        self.assertEquals(users.count(), 2)

    def test_get_aliment(self):
        aliment = Aliment.objects.get(user_set=self.user_1)
        self.assertEqual('fromage', aliment.name)
