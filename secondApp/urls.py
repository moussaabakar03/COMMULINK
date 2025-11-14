from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),

    #---------------------URLS EVENEMENTS---------------------
    path('listeCategorie/', views.listeCategorie, name='listeCategorie'),
    path('ajoutTypeEvenement/', views.ajoutTypeEvenement, name='ajoutTypeEvenement'),
    path('affichageEvenement/', views.affichageEvenement, name='affichageEvenement'),
    path('ajoutEvenement/', views.ajoutEvenement, name='ajoutEvenement'),
    path('detailEvenements/<int:id>', views.detailEvenements, name='detailEvenements'),
    path('evenementFiltrer/<int:id>', views.evenementFiltrer, name='evenementFiltrer'),
    path('modifierCategorie/<int:id>', views.modifierCategorie, name='modifierCategorie'),
    path('supprimerCategorie/<int:id>', views.supprimerCategorie, name='supprimerCategorie'),
    path('modifierEvenement/<int:id>', views.modifierEvenement, name='modifierEvenement'),
    path('supprimerEvenement/<int:id>', views.supprimerEvenement, name='supprimerEvenement'),
    
    path('depublier-evenement/<int:id>', views.depublier_evenement, name='depublier_evenement'),
    path('publier-evenement/<int:id>', views.publier_evenement, name='publier_evenement'),
    
    
    
    #----------------------URLS TEMOIGNAGES--------------------------------
    path('ajoutTemoingnages/', views.ajoutTemoingnages, name='ajoutTemoingnages'),
    path('temoingnages/', views.listeTemoingnes, name='temoingnages'),
    path('modifierTemoingnes/<int:id>', views.modifierTemoingnes, name='modifierTemoingnes'),
    path('supprimerTemoingne/<int:id>', views.supprimerTemoingne, name='supprimerTemoingne'),

    #-----------------------URLS MEMBRES-------------------------------
    path('liste-des-membres', views.liste_membres, name='liste_membres'),
    path('creer/', views.creer_membre, name='creer_membre'),
    path('membre/<int:pk>/', views.detail_membre, name='detail_membre'),
    path('membre/<int:pk>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('<int:pk>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
    
    
    path('ajoutMembreEquipe/', views.ajoutMembreEquipe, name='ajoutMembreEquipe'),
    path('liste-EquipeDirigeante/', views.liste_EquipeDirigeante, name='liste_EquipeDirigeante'),
    path('<int:pk>/modification-MembreEquipeDirigeante/', views.modification_MembreEquipeDirigeante, name='modification_MembreEquipeDirigeante'),
    path('<int:pk>/supprimer-MembreEquipe/', views.supprimer_MembreEquipe, name='supprimer_MembreEquipe'),
    
    

    #------------------------URLS ANNONCES------------------------------------
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/creer/', views.creer_annonce, name='creer_annonce'),
    path('annonces/modifier/<int:id>/', views.modifier_annonce, name='modifier_annonce'),
    path('annonces/publier/<int:id>/', views.publier_annonce, name='publier_annonce'),
    path('annonces/supprimer/<int:id>/', views.supprimer_annonce, name='supprimer_annonce'),



    #-----------------------------URLS Annees------------------------------------
    path('liste-annee/', views.listeAnnee, name='listeAnnee'),
    path('ajout-annee/', views.ajoutAnnee, name='ajoutAnnee'),
    
    
    
    #-----------------------------URLS PAIEMENTS------------------------------------
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/ajouter/', views.ajouter_paiement, name='ajouter_paiement'),
    path('paiements/rappeler/', views.rappeler_paiements, name='rappeler_paiements'),
    path('<int:pk>/modifierPaiement/', views.modifierPaiement, name='modifierPaiement'),
    path('<int:pk>/paiementParEvenement/', views.paiementParEvenement, name='paiementParEvenement'),
    
    
    
    path('reinscriptionUser/', views.reinscriptionUser, name='reinscriptionUser'),
    

]
