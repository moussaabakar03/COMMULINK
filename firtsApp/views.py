from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from commulink.utils.decorators import admin_required, membre_required
from firtsApp.forms import ConnexionForm, MembreInscriptionForm
from secondApp.models import EquipeDirigeante, Evenement, EvenementImage, EvenementVideo, Membre, Paiement, Reinscription, Temoingnage, TypeEvenement
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.contrib import messages



from datetime import datetime
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import os
from django.conf import settings



# Create your views here.





from django.contrib.auth import authenticate, login, logout



def connexion(request):
    next_url = request.GET.get("next")  

    if request.method == "POST":
        form = ConnexionForm(request.POST, request=request)

        if form.is_valid():
            utilisateur = form.get_user()
            login(request, utilisateur)

            # Si next existe, redirection prioritaire
            if next_url:
                return redirect(next_url)

            # 3️Sinon, ton comportement normal
            if utilisateur.is_superuser or utilisateur.role == "membreEquipe":
                messages.success(request, f"Bienvenue 'Admin' ")
                return redirect(reverse('admin_dashboard'))
            
            elif utilisateur.role == "membreLambda":
                membre = get_object_or_404(Membre, utilisateur=utilisateur)
                messages.success(request, f"Bienvenue {membre.nom} {membre.prenom}")
                return redirect("index")

        else:
            messages.error(request, "Identifiant ou mot de passe incorrect")

    else:
        form = ConnexionForm()

    return render(request, 'user/connexion.html', {"form": form})


def deconnexion(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté avec succès!")
    return redirect("index")


def index(request):
    evenements = Evenement.objects.all().order_by('id')[:5]
    typeEvenement = TypeEvenement.objects.all()
    equipes = EquipeDirigeante.objects.all()
    temoingnages = Temoingnage.objects.all()
    return render(request, 'user/accueil.html', {'evenements': evenements, 'typeEvenement': typeEvenement, 'equipes': equipes, 'temoingnages': temoingnages})

def contact(request):
    return render(request, 'user/contact.html')

def feteIs(request):
    return render(request, 'user/feteIs.html')

# def inscription(request):
#     return render(request, 'user/inscription.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def inscription_membre(request):
    """
    Inscription publique - Crée une demande en attente de validation
    """
    if request.method == 'POST':
        form = MembreInscriptionForm(request.POST, request.FILES)
        
        # Debug: Afficher les erreurs de validation
        if not form.is_valid():
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            
            return render(request, 'user/formulaireInscription.html', {
                'form': form,
                'titre': "Demande d'inscription"
            })
        
        try:
            # Créer le membre avec statut "en_attente"
            membre = form.save(commit=False)
            membre.statut = 'en_attente'
            membre.utilisateur = None
            
            # Valider qu'au moins un champ d'identité est rempli
            identite_fields = ['ner', 'keri', 'keribour', 'keriBa', 'keribourBa']
            has_identite = any(
                form.cleaned_data.get(field) 
                for field in identite_fields
            )
            
            if not has_identite:
                messages.error(
                    request, 
                    "Veuillez remplir au moins un des champs d'identité (Ner, Keri, Keribour, Keri Bâ, ou Keribour Bâ)."
                )
                return render(request, 'user/formulaireInscription.html', {
                    'form': form,
                    'titre': "Demande d'inscription"
                })
            
            membre.save()
            
            messages.success(
                request, 
                f"Merci {membre.prenom} ! Votre demande d'inscription a été envoyée avec succès. "
                f"Elle sera examinée par notre équipe dans les plus brefs délais."
            )
            return redirect('index')
            
        except IntegrityError as e:
            messages.error(
                request, 
                "Cette adresse email est déjà utilisée. Veuillez en choisir une autre."
            )
            return render(request, 'user/formulaireInscription.html', {
                'form': form,
                'titre': "Demande d'inscription"
            })
            
        except Exception as e:
            print(f"ERREUR: {str(e)}")
            messages.error(
                request, 
                f"Une erreur est survenue lors de l'inscription. Veuillez réessayer."
            )
            return render(request, 'user/formulaireInscription.html', {
                'form': form,
                'titre': "Demande d'inscription"
            })
    else:
        form = MembreInscriptionForm()
    
    return render(request, 'user/formulaireInscription.html', {
        'form': form,
        'titre': "Demande d'inscription"
    })
    
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView
from .forms import MembreForm

# class InscriptionMembreView(FormView):
#     template_name = 'user/formulaireInscription.html'
#     form_class = MembreForm
    
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
    
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
        
#         if form.is_valid():
#             try:
#                 # Sauvegarder le membre
#                 membre = form.save()
                
#                 messages.success(request, 
#                     f"Le membre {membre.nom_complet} a été inscrit avec succès !")
#                 return redirect('liste_membres')  # Ou une autre page
                
#             except Exception as e:
#                 messages.error(request, 
#                     f"Une erreur est survenue lors de l'inscription: {str(e)}")
#                 return render(request, self.template_name, {'form': form})
        
#         messages.error(request, 
#             "Veuillez corriger les erreurs dans le formulaire.")
#         return render(request, self.template_name, {'form': form})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Inscription - COMMULINK'
#         return context




def affichageEvenement(request, id):  
    evenement = TypeEvenement.objects.get(id = id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id, est_publie = True)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})


@login_required
def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    
    # Récupérer toutes les vidéos de l'événement
    evenementVideos = EvenementVideo.objects.filter(
        evenement=evenement
    ).order_by('-date_ajout')
    
    temoingnages = Temoingnage.objects.filter(evenement=evenement).order_by('-id')
    
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage, 'evenementVideos': evenementVideos, 'temoingnages': temoingnages,})





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


def liste_evenements(request):
    """
    Vue pour afficher la liste des types d'événements avec statistiques
    ET les  événements
    """
    # Récupérer tous les types d'événements
    type_evenements = TypeEvenement.objects.all().order_by('nom_type_evenement')
    
    # Récupérer les  événements 
    Evenements = Evenement.objects.all().order_by('-dateHeure')
    
    # Calculer les statistiques pour le hero
    total_events = Evenement.objects.count()
    now = datetime.now()
    upcoming_events = Evenement.objects.filter(dateHeure__gte=now).count()
    
    context = {
        'typeEvenement': type_evenements,      # Pour la boucle des types d'événements
        'evenements': Evenements,     
        'total_events': total_events,          # Pour les statistiques
        'upcoming_events': upcoming_events,    # Pour les statistiques
    }
    return render(request, 'user/listeEvenement.html', context)


@login_required
@membre_required
def profil_membre(request):
    """Afficher le profil d'un membre"""
    if request.user.role != "membreLambda":
        return redirect("index")
    membre = get_object_or_404(Membre, utilisateur=request.user)
    reinscription = Reinscription.objects.filter(membre=membre).last()
    
    reinscriptions = Reinscription.objects.filter(membre=membre).order_by("-annee")
    paiements= Paiement.objects.filter(membre_Reinscris__in=reinscriptions)
    
    context = {
        'reinscription':reinscription,
        'membre': membre,
        'page_title': f'Profil - {membre.nom_complet}',
        'genres': Membre.GENRE_CHOICES,
        'paiements': paiements
        
    }
    
    return render(request, 'user/profil.html', context)


    
  


@login_required
def modifier_profil(request):
    """Modifier les informations du profil"""
    membre = get_object_or_404(Membre, utilisateur=request.user)
    
    
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
                    return redirect('profil_membre')
                
                if len(data['prenom']) < 2:
                    messages.error(request, 'Le prénom doit contenir au moins 2 caractères')
                    return redirect('profil_membre')
                
                if len(data['profession']) < 2:
                    messages.error(request, 'La profession doit contenir au moins 2 caractères')
                    return redirect('profil_membre')
                
                # Validation email
                try:
                    validate_email(data['email'])
                except ValidationError:
                    messages.error(request, 'Veuillez entrer une adresse email valide')
                    return redirect('profil_membre')
                
                # Vérifier l'unicité de l'email
                if Membre.objects.filter(email=data['email']).exclude(pk=membre.pk).exists():
                    messages.error(request, 'Cet email est déjà utilisé par un autre membre')
                    return redirect('profil_membre')
                
                # Mettre à jour les champs
                for field, value in data.items():
                    setattr(membre, field, value)
                
                membre.save()
                messages.success(request, 'Profil mis à jour avec succès!')
                
        except Exception as e:
            messages.error(request, f'Une erreur est survenue: {str(e)}')
    
    return redirect('profil_membre')


@login_required
def modifier_photo_profil(request):
    """Modifier la photo de profil d'un membre"""
    membre = get_object_or_404(Membre, utilisateur=request.user)
    
    if request.method == 'POST':
        try:
            nouvelle_photo = request.FILES.get('photo')
            
            if nouvelle_photo:
                # Vérifier la taille (max 5MB)
                if nouvelle_photo.size > 5 * 1024 * 1024:
                    messages.error(request, 'La photo ne doit pas dépasser 5MB')
                    return redirect('profil_membre')
                
                # Vérifier le type de fichier
                allowed_types = ['image/jpeg', 'image/png', 'image/gif']
                if nouvelle_photo.content_type not in allowed_types:
                    messages.error(request, 'Format de fichier non supporté. Utilisez JPG, PNG ou GIF.')
                    return redirect('profil_membre')
                
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
    
    return redirect('profil_membre')


