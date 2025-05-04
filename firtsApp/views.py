from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'user/accueil.html')

def contact(request):
    return render(request, 'user/contact.html')


def soireeCulturelle(request):
    return render(request, 'user/soireeCulturelle.html')

def journeeIntegration(request):
    return render(request, 'user/journeeIntegration.html')

def feteIs(request):
    return render(request, 'user/feteIs.html')

def formulaireInformation(request):
    return render(request, 'user/formulaireInformation.html')

def inscription(request):
    return render(request, 'user/inscription.html')

def connexion(request):
    return render(request, 'user/connexion.html')


