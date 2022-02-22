from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', ClientViewSet, basename='user')
router.register('clients', ProfileViewSet, basename='client')
router.register('messages', ClientSmsViewSet, basename='message')
router.register('plans', PlanViewSet, basename='plan')
router.register('souscriptions', SouscriptionViewSet, basename='souscription')
router.register('payements', PayementViewSet, basename='payement')
router.register('configs', ConfigViewSet, basename='config')
router.register('sms', SmsViewSet, basename='sms')

urlpatterns = [
    path('apiwassa/login/', login, name='login'),
    path('apiwassa/', include(router.urls)),
    # path('apiwassa/alimentation/', alimentationActif),
]
