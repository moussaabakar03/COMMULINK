from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminis/', views.admin, name='admin'),
    path('contact/', views.contact, name='contact'),
    path('soireeCulturelle/', views.soireeCulturelle, name='soireeCulturelle'),
    path('feteIs/', views.feteIs, name='feteIs'),
    path('formulaireInformation/', views.formulaireInformation, name='formulaireInformation'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    
    
    path('affichageEvenement/<int:id>/', views.affichageEvenement, name='affichageEvenement'),
    path('detailEvenement/<int:id>/', views.detailEvenement, name='detailEvenement'),    
    
]
