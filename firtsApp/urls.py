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
    
    
   path('evenements/<int:type_id>/', views.affichageEvenement, name='affichage_evenement'),

    path('detailEvenement/<int:id>/', views.detailEvenement, name='detailEvenement'),    
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('faq/', views.FAQView.as_view(), name='faq'),

    path('evenements/', views.liste_evenements, name='liste_evenements'),
    path('evenements/<int:type_id>/', views.affichageEvenement, name='affichageEvenement'),
      
    path('profil/<int:pk>/', views.profil_membre, name='profil_membre'),
    path('profil/<int:pk>/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/<int:pk>/modifier-photo/', views.modifier_photo_profil, name='modifier_photo_profil'),
   
    
]
