from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('caesar-cipher/',views.caesar_cipher),
    path('hill-cipher/',views.hill_cipher),
    path('playfair-cipher/',views.playfair_cipher),
    path('vignere-cipher/',views.vignere_cipher),
    path('rsa-cipher/',views.rsa_cipher),
    path('elgamal-cipher/',views.elgamal_cipher),
]