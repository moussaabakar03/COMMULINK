from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('feteIs/', views.feteIs, name='feteIs'),
    path('inscription/confirmation/<int:pk>/', views.inscription_confirmation, name='inscription_confirmation'),
    path('inscription/', views.inscription_membre, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    
    
    path('affichageEvenement/<int:id>/', views.affichageEvenement, name='affichageEvenement'),
    path('detailEvenement/<int:id>/', views.detailEvenement, name='detailEvenement'),    
    
]
