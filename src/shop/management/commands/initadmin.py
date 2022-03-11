from django.contrib.auth.models import User
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = 'tilek'
                email = 'admin@gmail.com'
                password = '1234567q'
                print('Creating account for %s (%s)' % (username, email))
                User.objects.create_superuser(
                    email=email, username=username, password=password)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
