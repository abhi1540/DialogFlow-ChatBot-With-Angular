from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib import admin
from mongoengine.document import Document
from mongoengine.fields import EmbeddedDocumentField, StringField,  DateTimeField
from mongoengine import connect, CASCADE
from django.conf import settings
from django.utils import timezone


connect(settings.DATABASES['default']['NAME'])
class CustomUser(models.Model):
    emailAddress = models.EmailField(max_length=250, verbose_name='Email Address')
    phone_num = PhoneNumberField()
    pincode = models.CharField(max_length=10)

    USERNAME_FIELD = 'emailAddress'
    REQUIRED_FIELDS = ['emailAddress', 'phone_num', 'pincode']



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('emailAddress', 'phone_num', 'pincode')


class Userconv(Document):
    session = StringField(max_length=500, blank=False)
    userconv = StringField(max_length=1000, blank=False)
    botconv = StringField(max_length=1000, blank=False)
    date = DateTimeField(default=timezone.now)

 
