from django.core.mail import send_mail, send_mass_mail
from .models import Order
from celery import shared_task, task
from myshop.settings import EMAIL_HOST_USER
from myshop.celery import app as celery_app
from celery.schedules import crontab, schedule


@shared_task
def order_created(order_id):
    print('sent')
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
        f'You have successfully placed an order.' \
        f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject=subject, message=message,
                          from_email=EMAIL_HOST_USER, recipient_list=[order.email], fail_silently=False)
    print('sent')
    return mail_sent


def key(e):
    subject = 'New collections in the shop now!'
    return (subject, f'Hi, {e.first_name}.\n\n \
        Our shop recieved new party of goods this week.\n\n \
            Check out it!\n', EMAIL_HOST_USER, (e.email,))


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=13, day_of_week=7),
        weakly_checkout_emails.s(),
    )


@celery_app.task
def weakly_checkout_emails():
    print('hello')
    orders = Order.objects.all()
    mails = list(map(key, orders))
    # remove duplicates
    mails = list(set([i for i in mails]))
    mails_sent = send_mass_mail(mails)
    return mails_sent
