from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('feteIs/', views.feteIs, name='feteIs'),
    path('inscription/', views.inscription_membre, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    
    # path('inscription/', views.InscriptionMembreView.as_view(), name='inscription'),
    
    path('affichageEvenement/<int:id>/', views.affichageEvenement, name='affichageEvenement'),
    path('detailEvenement/<int:id>/', views.detailEvenement, name='detailEvenement'),    
    
    
    path('detailEvenement/<int:id>/', views.detailEvenement, name='detailEvenement'),    
    path('a-propos/', views.AboutView.as_view(), name='about'),
    path('faq/', views.FAQView.as_view(), name='faq'),

    path('evenements/', views.liste_evenements, name='liste_evenements'),
    path('evenements/<int:type_id>/', views.modifier_photo_profil, name='affichageEvenement'),
      
    path('profil/', views.profil_membre, name='profil_membre'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/modifier-photo/', views.modifier_photo_profil, name='modifier_photo_profil'),
    
]
