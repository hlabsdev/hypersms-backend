from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class ConfigInline(admin.StackedInline):
    model = Config
    can_delete = False
    extra = 0
    verbose_name = ("Config")
    verbose_name_plural = ("Configs")
    
    def __str__(self):
        return self.model.entete

class SouscriptionInline(admin.StackedInline):
    model = Souscription
    can_delete = True
    extra = 0
    max_num = 1
    verbose_name = ("Souscription")
    verbose_name_plural = ("Souscriptions")
    
    def __str__(self):
        return f"Souscription: {self.model.entete}, Plan: {self.model.plan.title}"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Client
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    inlines = [SouscriptionInline, ConfigInline]


admin.site.register(Client, CustomUserAdmin)
admin.site.register(Config)
admin.site.register(Plan)
admin.site.register(Souscription)
admin.site.register(Payement)
admin.site.register(Sms)