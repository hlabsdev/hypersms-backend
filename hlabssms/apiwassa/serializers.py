# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from .models import *

""" Base Serializers start """
""" Base Serializers end """

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})
                
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["url", "id", "username", "password", "name", "contact", "email", "adress", "profile", "is_active"]
        read_only_fields = ["is_active"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['id', 'entete', 'client', 'is_default', 'is_actif']
        read_only_fields = ["is_actif"]
        
                
class PayementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement
        fields = ['id', 'libelle', 'amount', 'date', 'payed', 'souscription']
        read_only_fields = ["payed"]
        
          
class SouscriptionSerializer(serializers.ModelSerializer):
    payements = PayementSerializer(many=True, read_only=True)
    class Meta:
        model = Souscription
        fields = ['id', 'numero', 'plan', 'client', 'date', 'nbr_sms_sent', 'nbr_sms_rem', 'to_be_payed', 'is_payed', 'is_actif', 'tag', 'payements']
        read_only_fields = ["numero", "to_be_payed", "is_payed", "is_actif", "nbr_sms_sent", "nbr_sms_rem"]
        
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'title', 'nbr_sms', 'price', 'tarif', 'is_actif']
        read_only_fields = ['is_actif', 'tarif']
        
        
class ProfileSerializer(serializers.ModelSerializer):
    entetes = ConfigSerializer(many=True, read_only=True)
    souscription = SouscriptionSerializer(read_only=True)
    
    class Meta:
        model = Client
        fields = ["url", "id", "username", "name", "contact", "email", "adress", "profile", "is_active", "souscription", "entetes"]
        read_only_fields = ["is_active"]
        
        
class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ['id', 'sender', 'receptor', 'text', 'date', 'client', 'taille', 'status']
        read_only_fields = ['status', 'taille']
        
        
class ClientSmsSerializer(serializers.ModelSerializer):
    sms = SmsSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = ["url", "id", "username", "name", "contact", "email", "adress", "profile", "is_active", "sms"]
        read_only_fields = ["is_staff"]
        
