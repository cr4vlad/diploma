from django.test import TestCase
from django.contrib.auth.models import User
from .models import Room, Participation
from . import views
'''
class IntegrationalTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Установка запускается 1 раз в начале
        User.objects.create(username='tester1', password='password')
        User.objects.create(username='tester2', password='password')
        Room.objects.create(owner=User.objects.get(username='tester1'), title='Room1', description='Room1 description')
        Room.objects.create(owner=User.objects.get(username='tester2'), title='Room2', description='Room2 description')
        Participation.objects.create(user=User.objects.get(username='tester1'), room=Room.objects.get(title='Room1'))
        Keyword.objects.create(room=Room.objects.get(title='Room1'), keyword='room1')
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
class ModelsTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='tester1', password='password')
        user1.save()
        Room.objects.create(owner=User.objects.get(username='tester1'), title='Room1', description='Room1 description')
        Participation.objects.create(user=User.objects.get(username='tester1'), room=Room.objects.get(title='Room1'))
        Keyword.objects.create(room=Room.objects.get(title='Room1'), keyword='room1')
        pass

    def roomStrTest(self):
        room = Room.objects.get(id=1)
        expected_object_name = '%s by %s' % (room.title, room.owner)
        self.assertEquals(expected_object_name, str(room))

    def participationStrTest(self):
        participation = Participation.objects.get(id=1)
        expected_object_name = '%s in %s' % (participation.user, participation.room)
        self.assertEquals(expected_object_name, str(participation))

    def keywordStrTest(self):
        keyword = Keyword.objects.get(id=1)
        expected_object_name = '(%s) : %s' % (keyword.room, keyword.keyword)
        self.assertEquals(expected_object_name, str(keyword))

class ViewsTestClass(TestCase):

    def getKeywordsTest(self):
        title = 'Tests string you wish I started'
        self.assertEquals(['test', 'str', 'wish', 'start'], get_keywords(title))