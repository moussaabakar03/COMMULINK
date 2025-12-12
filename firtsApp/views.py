from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import EquipeDirigeante, Evenement, EvenementImage, Temoingnage, TypeEvenement

# Create your views here.


def index(request):
    evenements = Evenement.objects.all().order_by('id')[:5]
    typeEvenement = TypeEvenement.objects.all()
    equipes = EquipeDirigeante.objects.all()
    temoingnages = Temoingnage.objects.all()
    return render(request, 'user/accueil.html', {'evenements': evenements, 'typeEvenement': typeEvenement, 'equipes': equipes, 'temoingnages': temoingnages})

def admin(request):
    return render(request, 'dynamiquePart/admin.html')

def contact(request):
    return render(request, 'user/contact.html')

def soireeCulturelle(request):
    return render(request, 'user/soireeCulturelle.html')

def feteIs(request):
    return render(request, 'user/feteIs.html')

def formulaireInformation(request):
    return render(request, 'user/formulaireInformation.html')

def inscription(request):
    return render(request, 'user/inscription.html')

def connexion(request):
    return render(request, 'user/connexion.html')

def affichageEvenement(request, type_id):  
    evenement = TypeEvenement.objects.get(id = type_id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = type_id)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})

def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage})



from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'user/apropos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'À Propos - CommuLink'
        return context

class FAQView(TemplateView):
    template_name = 'user/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'FAQ - CommuLink'
        return context

from django.shortcuts import render
from datetime import datetime
from .models import TypeEvenement, Evenement

def liste_evenements(request):
    """
    Vue pour afficher la liste des types d'événements avec statistiques
    ET les  événements
    """
    # Récupérer tous les types d'événements
    type_evenements = TypeEvenement.objects.all().order_by('nom_type_evenement')
    
    # Récupérer les  événements 
    derniers_evenements = Evenement.objects.all().order_by('-dateHeure')
    
    # Calculer les statistiques pour le hero
    total_events = Evenement.objects.count()
    now = datetime.now()
    upcoming_events = Evenement.objects.filter(dateHeure__gte=now).count()
    
    context = {
        'typeEvenement': type_evenements,      # Pour la boucle des types d'événements
        'evenements': derniers_evenements,     # Pour la section "DERNIERS EVENEMENTS"
        'total_events': total_events,          # Pour les statistiques
        'upcoming_events': upcoming_events,    # Pour les statistiques
    }
    return render(request, 'user/listeEvenement.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from secondApp.models import Membre

import os
from django.conf import settings

@login_required
def profil_membre(request, pk):
    """Afficher le profil d'un membre"""
    membre = get_object_or_404(Membre, pk=pk)
    
    context = {
        'membre': membre,
        'page_title': f'Profil - {membre.nom_complet}',
        'genres': Membre.GENRE_CHOICES,
    }
    
    return render(request, 'membres/profil.html', context)

@login_required
def modifier_profil(request, pk):
    """Modifier les informations du profil"""
    membre = get_object_or_404(Membre, pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Récupérer et nettoyer les données
                data = {}
                for field in ['nom', 'prenom', 'sexe', 'email', 'telephone', 'adresse', 
                             'profession', 'numeroUrgence', 'niveauEtude', 'ecole',
                             'ner', 'keri', 'keribour', 'keriBa', 'keribourBa', 'notes']:
                    value = request.POST.get(field, '').strip()
                    data[field] = value if value != '' else None
                
                # Validation
                if len(data['nom']) < 2:
                    messages.error(request, 'Le nom doit contenir au moins 2 caractères')
                    return redirect('profil_membre', pk=pk)
                
                if len(data['prenom']) < 2:
                    messages.error(request, 'Le prénom doit contenir au moins 2 caractères')
                    return redirect('profil_membre', pk=pk)
                
                if len(data['profession']) < 2:
                    messages.error(request, 'La profession doit contenir au moins 2 caractères')
                    return redirect('profil_membre', pk=pk)
                
                # Validation email
                try:
                    validate_email(data['email'])
                except ValidationError:
                    messages.error(request, 'Veuillez entrer une adresse email valide')
                    return redirect('profil_membre', pk=pk)
                
                # Vérifier l'unicité de l'email
                if Membre.objects.filter(email=data['email']).exclude(pk=membre.pk).exists():
                    messages.error(request, 'Cet email est déjà utilisé par un autre membre')
                    return redirect('profil_membre', pk=pk)
                
                # Mettre à jour les champs
                for field, value in data.items():
                    setattr(membre, field, value)
                
                membre.save()
                messages.success(request, 'Profil mis à jour avec succès!')
                
        except Exception as e:
            messages.error(request, f'Une erreur est survenue: {str(e)}')
    
    return redirect('profil_membre', pk=pk)

@login_required
def modifier_photo_profil(request, pk):
    """Modifier la photo de profil d'un membre"""
    membre = get_object_or_404(Membre, pk=pk)
    
    if request.method == 'POST':
        try:
            nouvelle_photo = request.FILES.get('photo')
            
            if nouvelle_photo:
                # Vérifier la taille (max 5MB)
                if nouvelle_photo.size > 5 * 1024 * 1024:
                    messages.error(request, 'La photo ne doit pas dépasser 5MB')
                    return redirect('profil_membre', pk=pk)
                
                # Vérifier le type de fichier
                allowed_types = ['image/jpeg', 'image/png', 'image/gif']
                if nouvelle_photo.content_type not in allowed_types:
                    messages.error(request, 'Format de fichier non supporté. Utilisez JPG, PNG ou GIF.')
                    return redirect('profil_membre', pk=pk)
                
                # Supprimer l'ancienne photo si elle existe
                if membre.photo:
                    old_photo_path = membre.photo.path
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                # Sauvegarder la nouvelle photo
                membre.photo = nouvelle_photo
                membre.save()
                
                messages.success(request, 'Photo de profil mise à jour avec succès!')
            else:
                messages.error(request, 'Veuillez sélectionner une photo.')
                
        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour de la photo: {str(e)}')
    
    return redirect('profil_membre', pk=pk)