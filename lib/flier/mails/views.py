from django.http import HttpResponseBadRequest
from django import shortcuts
from flier.mails import models


def click(request, mail, recipient, message_id):
    click = models.MailClick.objects.click(mail, recipient, message_id)
    if click:
        return shortcuts.redirect(click.mail.click_url)
    return HttpResponseBadRequest()
