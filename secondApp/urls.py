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
    # Liste et détails
    path('equipe', views.liste_equipe_dirigeante, name='liste_equipe'),
    
    
    # Liste des membres
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    path('membres/<int:pk>/', views.detail_membre, name='detail_membre'),
    path('membres/<int:pk>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('membres/<int:pk>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
    path('membres/export-pdf/', views.exporter_membres_pdf, name='exporter_membres_pdf'),
    path('membres/export-csv/', views.exporter_membres_csv, name='exporter_membres_csv'),
    
    # Validation des inscriptions (non-AJAX)
    path('membres/<int:pk>/valider/', views.valider_membre, name='valider_membre'),
    path('membres/<int:pk>/refuser/', views.refuser_membre, name='refuser_membre'),
    
    # Validation AJAX
    path('membres/<int:pk>/valider-ajax/', views.valider_membre_ajax, name='valider_membre_ajax'),
    path('membres/<int:pk>/refuser-ajax/', views.refuser_membre_ajax, name='refuser_membre_ajax'),
    
    # Validation en masse
    path('membres/valider-tous/', views.valider_tous_en_attente, name='valider_tous_en_attente'),

    # API
    path('api/verifier-email/', views.verifier_email_disponible, name='verifier_email'),
    

    #------------------------URLS ANNONCES------------------------------------
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/creer/', views.creer_annonce, name='creer_annonce'),
    path('annonces/modifier/<int:id>/', views.modifier_annonce, name='modifier_annonce'),
    path('annonces/publier/<int:id>/', views.publier_annonce, name='publier_annonce'),
    path('annonces/depublier/<int:id>/', views.depublier_annonce, name='depublier_annonce'),
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
