from re import T
from celery import shared_task
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template
from datetime import date

from .models import Dava


@shared_task
def send_email(email):
    import logging

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    subject = 'Celery Report'
    from_email = 'umutdollaz@gmail.com'
    cond_met= False

    # write condition func
    today = date.today()
    davalar = Dava.objects.filter(deadline1__lt = today)
    if davalar:
        cond_met = True

    message = 'Task executed'

    if subject and message and from_email and cond_met:
        try:
            send_mail(subject, message, from_email, ['umut.toparlak@gmail.com'])
        except BadHeaderError:
            # change with loggers
            print('Invalid header found.')
        logging.info('sample sent to {email}')

@shared_task
def send_custom_email():
    """
    Send email to managers with weekly report info.
    # TODO:for executing multiple times use eval for some date range in scheduled task
    """
    #davalar = Dava.objects.filter(deadline1__lt = today)
    #dava_dict = {'davalar':list(Dava.objects.filter(deadline1__lt = today))}
    today = date.today()
    template = get_template("posta/mail.html")

    for manager in Dava.objects.values_list('manager_mail', flat=True).distinct():
   
        if davalar := Dava.objects.filter(manager_mail=manager, deadline1__lt = today):

            dava_dict = {'davalar':list(davalar)}
            message = template.render(dava_dict)

            mail = EmailMessage(
                subject="Weekly Report",
                body=message,
                from_email = 'umutdollaz@gmail.com',
                to=[manager]
            )
            mail.content_subtype = "html"

            try:
                mail.send()
            except BadHeaderError:
                print('Invalid header found.')

        #return mail.send()

