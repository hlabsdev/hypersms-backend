# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.utils import timezone
from .managers import *
from django.utils.translation import gettext_lazy as _
from random import randint


def random_with(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    

# Create your models here.
# My  models Managers

class TimeModel(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField("Date de création", blank=True, null=True)
    updated_at = models.DateTimeField("Date de mise ajour", blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    deleted_at = models.DateTimeField("Date de suppression", blank=True, null=True)
    
    objects = TimeModelManager()
    deleted_objects = DeletedTimeModelManager()

    def suppress(self):
        self.deleted = True
        self.deleted_at = timezone.now
        self.save()

    def restore(self):
        self.deleted = False
        self.deleted_at = None
        self.save()
        
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now
        # super().delete(*args, **kwargs)



class Client(TimeModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Nom d'utilisateur", max_length=250,  unique=True)
    email = models.EmailField('Adresse mail', blank=True, null=True)
    name = models.CharField("Nom Complet", max_length=250, blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=11, unique=True, null=True, blank=True, help_text="22891025263")
    auth_code = models.IntegerField("Code d'authentification", default=random_with(5), null=True, blank=True)
    profile = models.ImageField(upload_to="User/Profile", blank=True, null=True, verbose_name="Avatar de profil")
    is_admin = models.BooleanField(default=False, blank=True, null=True)
    # BaseUserFields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["name", "contact"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.name

class Config(TimeModel):
    entete = models.CharField("Entete des SMS", max_length=11, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='entetes', blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    is_actif = models.BooleanField(default=False, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.client.entetes.count() <=0:
            self.is_default = True
            self.is_actif = True
        else:
            self.is_default = False
        super().save(*args, **kwargs)
        
    def __str__(self):
        # return f"{self.id}"+"Actif" if self.is_actif else "Non Actif"
        return f"{self.entete}"+"Actif" if self.is_actif else "Non Actif"
        
class Plan(TimeModel):
    title = models.CharField("Libelle",max_length=250, blank=True, null=True)
    nbr_sms = models.IntegerField("Nombre de messages",blank=True, null=True)
    price = models.IntegerField("Prix",blank=True, null=True)
    tarif = models.CharField("Tarif",max_length=250, blank=True, null=True)
    is_actif = models.BooleanField(default=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        tar = (self.price / self.nbr_sms).__ceil__()
        self.tarif = f"{tar} Frcs/SMS"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Plan {self.title}: {self.nbr_sms} SMS à {self.price}"

class Souscription(TimeModel):
    CHOIX_TAG = (
        (1, 'BASIC'),
        (3, 'BRONZE'),
        (5, 'SILVER'),
        (7, 'GOLD'),
        (10, 'DIAMOND'),
        (0, 'NO LIMIT'),
    )
    numero = models.IntegerField(blank=True, null=True, default=random_with(6))
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='souscriptions', blank=True, null=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='souscription', blank=True, null=True)
    date = models.DateTimeField("Date de souscription", blank=True, null=True)
    nbr_sms_sent = models.IntegerField("Nombre de sms envoyé", default=0, blank=True, null=True)
    nbr_sms_rem = models.IntegerField("Nombre de sms restant", blank=True, null=True)
    to_be_payed = models.IntegerField("A payer",blank=True, null=True)
    is_payed = models.BooleanField(default=True, blank=True, null=True)
    is_actif = models.BooleanField(default=True, blank=True, null=True)
    tag = models.IntegerField(choices=CHOIX_TAG, default=1, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.nbr_sms_rem is None or self.nbr_sms_rem==0:
            self.nbr_sms_rem = self.plan.nbr_sms
        super().save(*args, **kwargs)
        
            
    def send_sms(self, len:int):
        sustract = (len/160).__ceil__()
        self.nbr_sms_sent +=sustract
        self.nbr_sms_rem -= sustract
        self.save()
        
    def change_tag(self, tag):
        self.tag = tag
        self.save()
        
    def __str__(self):
        return f"Souscription {self.numero} de: {self.client.name}, le {self.date}"

class Payement(TimeModel):
    libelle = models.CharField("Libelle du payement", max_length=250, blank=True, null=True)
    amount = models.IntegerField("Nombre de sms restant", blank=True, null=True)
    date = models.DateTimeField("Date de souscription", blank=True, null=True)
    payed = models.BooleanField(default=False, blank=True, null=True)
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE, related_name='payements', blank=True, null=True)

    def __str__(self):
        return f"Payement {self.libele} de {self.amount} pour {self.souscription.numero} effectué le: {self.date}"
    
class Sms(TimeModel):    
    CHOIX_STATUS = (
        (1, 'Delivré'),
        (2, 'Echoué'),
        (3, 'En Attente'),
    )
    sender = models.CharField("Entete",  max_length=250, blank=True, null=True)
    receptor = models.CharField("Numero du recepteur", max_length=250, blank=True, null=True)
    text = models.TextField("Texte", blank=True, null=True)
    date = models.DateTimeField("Date d'envoie", auto_now_add=True, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sms', blank=True, null=True)
    taille = models.CharField("Taille du sms", max_length=250, blank=True, null=True)
    status = models.IntegerField(choices=CHOIX_STATUS, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        nbcr = self.text.__len__()
        count = (nbcr/160).__ceil__()
        self.taille = f"{nbcr} Carateres, equivalent à {count} sms"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"De {self.sender} à {self.receptor}: {self.text[0:26]}"
    