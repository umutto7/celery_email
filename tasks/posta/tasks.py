from re import T
from celery import shared_task
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template
from datetime import date
from django.forms.models import model_to_dict
from rest_framework import serializers

from .models import Dava

class DavaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dava
        fields = "__all__"


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
    today = date.today()
    davalar = Dava.objects.filter(deadline1__lt = today)
    #dava_dict = {'davalar':list(Dava.objects.filter(deadline1__lt = today))}
    template = get_template("posta/mail.html")

    # TODO:build the logic for sending the mails to related managers 
    for manager in Dava.objects.values_list('manager_mail', flat=True).distinct():

        davalar = Dava.objects.filter(manager_mail=manager, deadline1__lt = today)
        if davalar:
            dava_dict = {'davalar':list(davalar)}
            message = template.render(dava_dict)

            mail = EmailMessage(
                subject="Weekly Report",
                body=message,
                from_email = 'umutdollaz@gmail.com',
                to=[manager]
            )
            mail.content_subtype = "html"

        #return mail.send()

