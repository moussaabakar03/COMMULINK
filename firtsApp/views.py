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

def ajoutTypeEvenement(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')
        description = request.POST.get('description')
        
        TypeEvenement.objects.create(
            nom_type_evenement=nom,  image_type_evenement=photo, description_type_evenement=description
        )
        return redirect('index')
    return render(request, 'dynamiquePart/ajoutTypeEvement.html')

def ajoutEvenement(request):
    typeEvenem = TypeEvenement.objects.all()
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_evenement = request.POST.get('type_evenement')
        images = request.FILES.getlist('photos[]') 
        
        evenementType = TypeEvenement.objects.get(id=type_evenement)
        
        
        if images:
            photoCouverture = images[0]
            evenement = Evenement.objects.create(
                typeEvenement= evenementType, titre=titre,  photo=photoCouverture, description=description
            )
            
            for image in range(0, len(images)):
                EvenementImage.objects.create(
                    evenement = evenement,
                    image = images[image]
                )
        return HttpResponseRedirect(reverse('index') + '#dernierEvenement')
    return render(request, 'dynamiquePart/ajoutEvenement.html', {'typeEvenem': typeEvenem})

def affichageEvenement(request, id):
    evenement = TypeEvenement.objects.get(id = id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})

def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage})

def ajoutMembreEquipe(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')
        role = request.POST.get('role')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        
        EquipeDirigeante.objects.create(
            nom = nom, image = photo, role = role, lienFacebook = facebook, lienInstagram = instagram , lienTwitter = twitter
        )
        return HttpResponseRedirect(reverse('index')+ '#equipeDirigeante')
    return render(request, 'dynamiquePart/ajoutMembreEquipe.html')

def ajoutTemoingnage(reqest):
    if reqest.method == 'POST':
        nom = reqest.POST.get('nom')
        image = reqest.FILES.get('image')
        message = reqest.POST.get('message')
        role = reqest.POST.get('role')
        
        Temoingnage.objects.create(
            nom = nom, image = image, message = message, role = role
        )
        return HttpResponseRedirect(reverse('index') + '#temoingnage')
    return render(reqest, 'dynamiquePart/ajoutTemoingnage.html')


