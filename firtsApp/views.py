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