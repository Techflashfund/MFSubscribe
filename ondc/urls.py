from django.urls import path
from .views import ondc_site_verification, on_subscribe

urlpatterns = [
    path('ondc-site-verification.html', ondc_site_verification, name='ondc_site_verification'),
    path('callback/on_subscribe', on_subscribe, name='on_subscribe')    
]
