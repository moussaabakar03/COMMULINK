from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from secondApp.models import EquipeDirigeante, Evenement, EvenementImage, Temoingnage, TypeEvenement

# Create your views here.

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

def connexion(request):
    return render(request, 'user/connexion.html')

def affichageEvenement(request, id):  
    evenement = TypeEvenement.objects.get(id = id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})

def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage})


