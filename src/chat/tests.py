from django.test import TestCase
from .models import Thread
from django.contrib.auth.models import User


class ThreadManagerTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='palo')
        user2 = User.objects.create(username='vata')
        admin = User.objects.create(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_two_ordinar_users_thread(self):
        user1 = User.objects.get(username='palo')
        user2 = User.objects.get(username='vata')
        user_ids = User.objects.values_list('id', flat=True)
        thread = Thread.objects.get_or_create_personal_thread(user1, user2)
        self.assertEqual(thread, None)

    def test_admin_user_thread(self):
        admin = User.objects.get(username='admin')
        user2 = User.objects.get(username='vata')
        user_ids = User.objects.values_list('id', flat=True)
        thread = Thread.objects.get_or_create_personal_thread(admin, user2)
        self.assertEqual(admin.is_superuser, True)
        self.assertEqual(thread.users.filter(
            id__in=user_ids).exists(), True)
        self.assertEqual(len(thread.users.filter(id__in=user_ids)), 2)
