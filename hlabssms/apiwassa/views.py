# -*- coding: utf-8 -*-

import environ
import requests
import urllib
""" Views for mobile API """
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets, permissions, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


env = environ.Env()
# reading .env file
environ.Env.read_env()
wassa_key = env("WASSA_KEY")
wassa_url = env("WASSA_URL")

def sendSms(sms:Sms):
    params = {
        "access-token": wassa_key,
        "sender": sms.sender,
        "receiver": sms.receptor,
        "text": sms.text.encode("utf-8")
    }
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe="", encoding="utf-8")

    response = requests.get(wassa_url, params=params)
    print(f"Response ==> {response}")
    print(f"Response decoded ==> {(response.json())}")
    print(f"Response status code ==> {response.status_code}")
    print(f"Response content ==> {response.content}")
    if response.status_code == 200:
        # if response.content[1].to == "success":
        return 1
        # elif response.content[1].__str__() == "failed " or response.content[1].__str__() == "error":
            #  return 2
        # else:
            # return 3
    return 2

# Create your views here.

""" Personal Status code
{
    0: Identifiant incorrects
    1: Compte non activée
    2: Saisies inavalide
    3: Erreur du serveur
    4: Message non envoyé
    5: Message en attente d'envoie
}
"""

@api_view(['POST'])
def login(request, format=None):
    """post user request"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        client = authenticate(
            username=serializer.data.get('username'),
            password=serializer.data.get('password'),
        )
        if client is not None:
            token = Token.objects.get_or_create(user=client)
            if client.is_active:
                serial_user = ProfileSerializer(client)
                return Response({'token': token.key, 'user': serial_user.data}, status=status.HTTP_200_OK)
            else:
                msg = "Votre compte n'est pas activée! Veuillez contacter le service clientele"
                return Response({'message': msg, "code":1})
        else:
            msg = 'Identifiants incorrects'
            return Response({'message': msg, "code":0})
    return Response({'message': serializer.errors, "code":2})


def get_user_by_token(token):
    token = token.split(' ')[1]
    try:
        user = Token.objects.get(key=token).user
    except Exception:
        user = None
    return user if user.is_active else None

# User Creation 
class ClientViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete clients """
    queryset = Client.objects.filter(deleted=False)
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Profile Management 
class ProfileViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Client.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OKstatus.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated], methods=['GET'])
    def get_deleted_list(self, request):
        objet = self.get_objects().deleted_objects.all().order_by('deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OKstatus.HTTP_200_OK)
    # Methodes suplementaire end

# ClientSms Management 
class ClientSmsViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Client.objects.filter(deleted=False)
    serializer_class = ClientSmsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Plan Management 
class PlanViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Plan.objects.filter(deleted=False)
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Souscription Management 
class SouscriptionViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Souscription.objects.filter(deleted=False)
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Payement Management 
class PayementViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Payement.objects.filter(deleted=False)
    serializer_class = PayementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Config Management 
class ConfigViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Config.objects.filter(deleted=False)
    serializer_class = ConfigSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end

# Sms Management 
class SmsViewSet(viewsets.ModelViewSet):
    """ Create, retrieve list and delete configs """
    queryset = Sms.objects.filter(deleted=False)
    serializer_class = SmsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        user = get_user_by_token(request.headers.get('Authorization'))
        if user:
            serializer = SmsSerializer(data=request.data)
            souscription = Souscription.objects.get(client=user)
            if serializer.is_valid():
                sms = Sms(
                    sender=request.data.get('sender'),
                    receptor=request.data.get('receptor'),
                    text=request.data.get('text'),
                    client=user
                )
                sent = sendSms(sms)
                sms.status = sent
                # serializer = SmsSerializer(sms)
                # if serializer.is_valid():
                # return Response({'message': serializer.errors, "code":3})
                sms.save()
                if sent == 1:
                    souscription.send_sms(sms.text.__len__())
                    return Response({'message':"message envoyé avec success", "sms": SmsSerializer(sms).data}, status=status.HTTP_200_OK)
                elif sent == 2:
                    return Response({'message':"échec au moment de l'envoie du message", "code":4})
                else:
                    souscription.send_sms(sms.text.__len__())
                    return Response({'message':"message en attente d'envoie", "code":5})
            return Response({'message': serializer.errors, "code":3})
        return Response({'message': "Not authorised", "code":3})
    
    # Methodes suplementaire start
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = self.get_object().deleted_objects.get(pk=pk)
        try:
            objet.restore()
            objet.save()
            return Response({'message': 'Les données ont été restaurées avec succes'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Erreur lors de la suppression', "code":3})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = self.get_object().deleted_objects.all().order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Methodes suplementaire end
