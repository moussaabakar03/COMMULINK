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
    
    path('evenements/videos/<int:video_id>/supprimer/', 
         views.supprimer_video_evenement, 
         name='supprimer_video_evenement'),
    
    
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
    path('liste-reinscription', views.liste_reinscriptions, name='listeReinscription'),
    path('reinscriptions/ajouter/', views.ajouter_reinscription, name='ajouter_reinscription'),
    path('reinscriptions/<int:pk>/supprimer/', views.supprimer_reinscription, name='supprimer_reinscription'),

    path('membres/export-pdf/', views.exporter_membres_pdf, name='exporter_membres_pdf'),
    path('membres/export-csv/', views.exporter_membres_csv, name='exporter_membres_csv'),
    
    
    path('membres/<int:pk>/valider/', views.valider_membre, name='valider_membre'),
    path('membres/<int:pk>/refuser/', views.refuser_membre, name='refuser_membre'),
    
    path('bloquer-membre/<int:pk>/refuser/', views.bloquerMembre, name='bloquerMembre'),
    path('debloquer-membre/<int:pk>/refuser/', views.debloquerMembre, name='debloquerMembre'),
    
    path('membres/valider-tous/', views.valider_tous_en_attente, name='valider_tous_en_attente'),
    
    
    path('ajoutMembreEquipe/', views.ajoutMembreEquipe, name='ajoutMembreEquipe'),
    path('liste-EquipeDirigeante/', views.liste_EquipeDirigeante, name='liste_EquipeDirigeante'),
    path('<int:pk>/modification-MembreEquipeDirigeante/', views.modification_MembreEquipeDirigeante, name='modification_MembreEquipeDirigeante'),
    path('<int:pk>/supprimer-MembreEquipe/', views.supprimer_MembreEquipe, name='supprimer_MembreEquipe'),
    
      # Publication/Dépublication
    path('equipe/toggle-publication/<int:pk>/', views.toggle_publication_membre, name='toggle_publication_membre'),
    path('equipe/publier-annee/<int:annee_id>/', views.publier_tous_membres_annee, name='publier_tous_membres_annee'),
    path('equipe/depublier-annee/<int:annee_id>/', views.depublier_tous_membres_annee, name='depublier_tous_membres_annee'),

    #------------------------URLS ANNONCES------------------------------------
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/creer/', views.creer_annonce, name='creer_annonce'),
    path('annonces/modifier/<int:id>/', views.modifier_annonce, name='modifier_annonce'),
    path('annonces/publier/<int:id>/', views.publier_annonce, name='publier_annonce'),
    path('annonces/supprimer/<int:id>/', views.supprimer_annonce, name='supprimer_annonce'),

    path('annonces/depublier/<int:id>/', views.depublier_annonce, name='depublier_annonce'),


    #-----------------------------URLS Annees------------------------------------
    path('liste-annee/', views.listeAnnee, name='listeAnnee'),
    path('ajout-annee/', views.ajoutAnnee, name='ajoutAnnee'),
    path('<int:pk>/modifier-annee/', views.modifierAnnee, name='modifierAnnee'),
    
    
    #-----------------------------URLS PAIEMENTS------------------------------------
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/ajouter/', views.ajouter_paiement, name='ajouter_paiement'),
    path('paiements/rappeler/', views.rappeler_paiements, name='rappeler_paiements'),
    path('<int:pk>/modifierPaiement/', views.modifierPaiement, name='modifierPaiement'),
    path('<int:pk>/paiementParEvenement/', views.paiementParEvenement, name='paiementParEvenement'),
    path('<int:pk>/ajout-Paiement-Evenement/', views.ajoutPaiementEvenement, name='ajoutPaiementEvenement'),
    path('<int:pk>/detail-paiment-membre/', views.detailPaimentMembre, name='detailPaimentMembre'),
    path('<int:pk_membre>/<int:pk_evenement>/supprimer-paiement/', views.supprimer_paiement, name='supprimer_paiement'),
    path('<int:pk>/supprimer-Paiement/', views.supprimerPaiement, name='supprimerPaiement'),
    
    
    
    path('reinscriptionUser/', views.reinscriptionUser, name='reinscriptionUser'),
    


    
    #------------------------------URLS RAPPORT-------------------------------------
    path('evenements/rapports/', views.liste_rapports_evenement, name='liste_rapports_evenement'),
    path('evenements/<int:pk>/rapport/', views.rapport_evenement_form, name='rapport_evenement_form'),
    path('evenements/<int:pk>/rapport/pdf/', views.rapport_evenement_pdf, name='rapport_evenement_pdf'),

]
