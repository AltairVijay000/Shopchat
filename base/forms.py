from dataclasses import fields
from inspect import ismethoddescriptor
from pyexpat import model
from turtle import mode
from django.forms import ModelForm
from .models import Offer
from django.contrib.auth.models import User
class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'
        exclude = ['host','participants']


class UserForm(ModelForm):
    class Meta:
        model=User
        fields= ['username', 'email']

