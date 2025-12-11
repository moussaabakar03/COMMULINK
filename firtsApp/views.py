from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from commulink.utils.decorators import admin_required, membre_required
from firtsApp.forms import ConnexionForm, MembreInscriptionForm
from secondApp.models import EquipeDirigeante, Evenement, EvenementImage, EvenementVideo, Membre, Temoingnage, TypeEvenement
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


from django.contrib.auth import authenticate, login, logout



def connexion(request):
    next_url = request.GET.get("next")  #  on récupère le paramètre next

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

def formulaireInformation(request):
    return render(request, 'user/formulaireInformation.html')

# def inscription(request):
#     return render(request, 'user/inscription.html')


def inscription_membre(request):
    """
    Inscription publique - Crée une demande en attente de validation
    """
    if request.method == 'POST':
        form = MembreInscriptionForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Créer le membre avec statut "en_attente"
                membre = Membre(
                    nom=form.cleaned_data['nom'],
                    prenom=form.cleaned_data['prenom'],
                    sexe=form.cleaned_data['sexe'],
                    email=form.cleaned_data['email'],
                    telephone=form.cleaned_data.get('telephone') or '',
                    adresse=form.cleaned_data.get('adresse') or '',
                    profession=form.cleaned_data['profession'],
                    numeroUrgence=form.cleaned_data.get('numeroUrgence') or '',
                    niveauEtude=form.cleaned_data.get('niveauEtude') or '',
                    ecole=form.cleaned_data.get('ecole') or '',
                    ner=form.cleaned_data.get('ner') or '',
                    keri=form.cleaned_data.get('keri') or '',
                    keribour=form.cleaned_data.get('keribour') or '',
                    keriBa=form.cleaned_data.get('keriBa') or '',
                    keribourBa=form.cleaned_data.get('keribourBa') or '',
                    notes=form.cleaned_data.get('notes') or '',
                    statut='en_attente',
                    utilisateur=None,
                )
                
                # Photo
                if form.cleaned_data.get('photo'):
                    membre.photo = form.cleaned_data['photo']
                
                membre.save()
                
                # Ajouter la filière dans les notes si présente
                filiere = form.cleaned_data.get('filiere', '')
                if filiere:
                    if membre.notes:
                        membre.notes += f"\nFilière: {filiere}"
                    else:
                        membre.notes = f"Filière: {filiere}"
                    membre.save()
                
                messages.success(
                    request, 
                    f"Merci {membre.prenom} ! Votre demande d'inscription a été envoyée avec succès. "
                    f"Elle sera examinée par notre équipe dans les plus brefs délais."
                )
                return redirect('inscription_confirmation', pk=membre.pk)
                
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreInscriptionForm()
    
    return render(request, 'user/inscription.html', {
        'form': form,
        'titre': "Demande d'inscription"
    })


def inscription_confirmation(request, pk):
    """Page de confirmation après inscription"""
    membre = get_object_or_404(Membre, pk=pk)
    
    return render(request, 'user/inscription_confirmation.html', {
        'membre': membre
    })


# def connexion(request):
#     return render(request, 'user/connexion.html')

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


