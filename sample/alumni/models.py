from django.db import models
from django.contrib.auth.models import User
from flier import models as flier_models
from flier.mails import (
    models as mails_models, methods as mails_methods)

# Create your models here.


class Reunion(models.Model):
    name = models.CharField(max_length=20, unique=True, db_index=True)
    sender = models.OneToOneField(flier_models.Sender)

    def __unicode__(self):
        return self.name


class Alumnus(models.Model):
    reunion = models.ForeignKey(Reunion)
    user = models.ForeignKey(
        User,
        null=True, default=None, blank=True, on_delete=models.SET_NULL)
    is_admin = models.BooleanField(default=False)
    address = models.EmailField(max_length=20)
    family_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)

    def __unicode__(self):
        return u"{0} {1}".format(self.first_name, self.family_name)

    @property
    def to(self):
        to, _ = flier_models.Address.objects.get_or_create(address=self.address)
        return to


class Letter(mails_models.Mail):
    reunion = models.ForeignKey(Reunion)

    def add_all(self):
        for a in self.reunion.alumnus_set.all():
            self.letterrecipient_set.get_or_create(
                key=self.reunion.sender.instance.verp(),
                to=a.to, alumnus=a, sender=self.reunion.sender)

    def excluded_alumni(self):
        '''
        - included LetterRecipient list : self.letterrecipient_set.all()
        '''
        return self.reunion.alumnus_set.exclude(letterrecipient__letter=self)


class LetterRecipient(flier_models.Recipient, mails_methods.Recipient):
    mail = models.ForeignKey(Letter)
    alumnus = models.ForeignKey(Alumnus)


class AdminLetter(mails_models.Mail):
    reunion = models.ForeignKey(Reunion)


class AdminLetterRecipient(flier_models.Recipient, mails_methods.Recipient):
    mail = models.ForeignKey(AdminLetter)
    alumnus = models.ForeignKey(Alumnus)
