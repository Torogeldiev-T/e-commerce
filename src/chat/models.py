from django.db import models
from django.db.models.aggregates import Count
PERSONAL_THREAD = 'personal'


class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, admin, second_user):
        if not second_user.is_authenticated:
            return None
        if admin != second_user:
            # return none if no one is admin
            if not admin.is_superuser and not second_user.is_superuser:
                return None
            # return existing thread with admin waiting for user if there is
            threads = self.get_queryset().filter(type=PERSONAL_THREAD)
            threads = threads.filter(
                users__in=[admin, second_user]).distinct()
            threads = threads.annotate(
                u_count=Count('users')).filter(u_count=2).filter(is_active=False)
            if threads.exists():
                return threads.first()
            admin_waiting_thread = self.get_queryset().filter(type=PERSONAL_THREAD).filter(
                users__in=[admin]).annotate(
                u_count=Count('users')).filter(u_count=1).filter(is_active=False).first()
            if admin_waiting_thread:
                admin_waiting_thread.users.add(second_user)
                return admin_waiting_thread
            else:
                thread = self.create(type=PERSONAL_THREAD, is_active=False)
                thread.users.add(admin)
                thread.users.add(second_user)
                return thread
        else:
            threads = self.get_queryset().filter(type=PERSONAL_THREAD)
            thread = threads.annotate(
                u_count=Count('users')).filter(u_count=2).filter(is_active=False).first()
            if thread:
                return thread
            thread = threads.annotate(u_count=Count('users')).filter(
                u_count=1).filter(is_active=False).first()
            if thread:
                return thread
            else:
                thread = self.create(type=PERSONAL_THREAD, is_active=False)
                thread.users.add(admin)
                return thread

    def get_by_user(self, user):
        return self.get_queryset().filter(users__in=[user])


class Thread(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)
    type = models.CharField(
        max_length=50, default=PERSONAL_THREAD, db_index=True)
    users = models.ManyToManyField('auth.User', db_index=True)
    is_active = models.BooleanField(db_index=True)

    objects = ThreadManager()
