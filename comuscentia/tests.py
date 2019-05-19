from django.test import TestCase
from django.contrib.auth.models import User
from .models import Room, Participation
from .forms import RoomForm
'''
class IntegrationalTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Установка запускается 1 раз в начале
        pass

    def setUp(self):
        # Установки запускаются перед каждым тестом
        pass

    def tearDown(self):
        # Очистка после каждого метода
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)
'''
class RoomModelTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='tester1', password='password')
        Room.objects.create(owner=User.objects.get(username='tester1'), title='Room1', description='Room1 description')
        pass

    def test_str(self):
        room = Room.objects.get(id=1)
        expected_object_name = '%s by %s' % (room.title, room.owner)
        self.assertEquals(expected_object_name, str(room))

    def test_close(self):
        room = Room.objects.get(id=1)
        self.assertEquals(False, room.close)