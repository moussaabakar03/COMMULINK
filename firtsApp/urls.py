from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('soireeCulturelle/', views.soireeCulturelle, name='soireeCulturelle'),
    path('journeeIntegration/', views.journeeIntegration, name='journeeIntegration'),
    path('feteIs/', views.feteIs, name='feteIs'),
    path('formulaireInformation/', views.formulaireInformation, name='formulaireInformation'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    
]
