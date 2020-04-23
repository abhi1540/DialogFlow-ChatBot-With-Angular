from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser, Userconv
from rest_framework_mongoengine.serializers import DocumentSerializer
from mongoengine.document import Document
from mongoengine.fields import EmbeddedDocumentField, StringField,  DateTimeField
from mongoengine import connect, CASCADE



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['emailAddress', 'phone_num', 'pincode']


class ConvSerializer(DocumentSerializer):
    class Meta:
        model = Userconv
        fields = ['session', 'userconv', 'botconv','date']
    def to_internal_value(self, data):
        return super(DocumentSerializer, self).to_internal_value(data)