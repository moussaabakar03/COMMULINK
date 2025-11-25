from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from commulink.utils.decorators import admin_required, membre_required
from firtsApp.forms import ConnexionForm
from secondApp.models import EquipeDirigeante, Evenement, EvenementImage, Membre, Temoingnage, TypeEvenement
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


from django.contrib.auth import authenticate, login, logout



def connexion(request):
    if request.method == "POST":
        form = ConnexionForm(request.POST, request=request)  

        if form.is_valid():
            utilisateur = form.get_user()
            login(request, utilisateur)

            if utilisateur.is_superuser or utilisateur.role == "membreEquipe":
                messages.success(request, f"Bienvenue {utilisateur}")
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

def inscription(request):
    return render(request, 'user/inscription.html')

# def connexion(request):
#     return render(request, 'user/connexion.html')

def affichageEvenement(request, id):  
    evenement = TypeEvenement.objects.get(id = id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})

@login_required
@membre_required
@admin_required
def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage})


