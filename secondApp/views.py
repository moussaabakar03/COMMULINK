from django.shortcuts import redirect, render

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Membre, Annonce, Paiement
from .forms import MembreForm, AnnonceForm, PaiementForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mass_mail
from firtsApp.models import TypeEvenement, Evenement, EquipeDirigeante, EvenementImage
from time import timezone
import datetime
# DASHBOARD VIEW
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from firtsApp.models import EquipeDirigeante, Evenement, EvenementImage, Temoingnage, TypeEvenement


# DASHBOARD VIEW

def admin_dashboard(request):
    return render(request, "admin/index.html")



#----------------------------------GESTION DES EVENEMENTS--------------------------------------

def listeCategorie(request):
    typeEvenement = TypeEvenement.objects.annotate(nombreEvenemnet=Count('evenement'))
    
    return render(request, 'admin/gestionEvenement/listeCategorie.html', {
        'typeEvenement': typeEvenement
    })

def ajoutTypeEvenement(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        photo = request.FILES.get('image')
        description = request.POST.get('description')
        
        TypeEvenement.objects.create(
            nom_type_evenement=nom,  image_type_evenement=photo, description_type_evenement=description
        )
        return redirect('listeCategorie')
    return render(request, 'admin/gestionEvenement/ajoutCategorie.html')


def modifierCategorie(request, id):
    categorie = get_object_or_404(TypeEvenement, pk=id)
    if request.method == 'POST':
        categorie.nom_type_evenement = request.POST.get('nom')
        categorie.image_type_evenement = request.FILES.get('photo')
        categorie.description_type_evenement = request.POST.get('description')
        categorie.save()

        return redirect('listeCategorie')
    return render(request, 'admin/gestionEvenement/modifierCategorie.html', { 'categorie': categorie })

def supprimerCategorie(request, id):
    categorie = get_object_or_404(TypeEvenement, pk=id)
    categorie.delete()
    return redirect('listeCategorie')

# def affichageEvenement(request, id):
#     evenement = TypeEvenement.objects.get(id = id)
#     evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
#     return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})


def affichageEvenement(request):
    evenements = Evenement.objects.all().order_by('-id')
    return render(request, 'admin/gestionEvenement/listeEvenement.html', {'evenements': evenements})

def ajoutEvenement(request):
    typeEvenem = TypeEvenement.objects.all()
    if request.method == "POST":
        # titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_evenement = request.POST.get('type_evenement')
        images = request.FILES.getlist('photos[]') 
        
        evenementType = TypeEvenement.objects.get(id=type_evenement)
        
        if images:
            photoCouverture = images[0]
            evenement = Evenement.objects.create(
                typeEvenement= evenementType, photo=photoCouverture, description=description
            )
            
            for image in range(0, len(images)):
                EvenementImage.objects.create(
                    evenement = evenement,
                    image = images[image]
                )
        return redirect('affichageEvenement')
    return render(request, 'admin/gestionEvenement/ajoutEvenement.html', {'typeEvenem': typeEvenem})

def evenementFiltrer(request, id):
    categorieEvenemnt = TypeEvenement.objects.get(id = id)
    evenements = Evenement.objects.filter(typeEvenement__id=id)
    return render(request, "admin/gestionEvenement/evenementFiltrer.html", {"evenements": evenements,"categorieEvenemnt": categorieEvenemnt})

def detailEvenements(request, id):
    evenement = Evenement.objects.get(id=id)
    
    temoingnages = Temoingnage.objects.filter(evenement = evenement)
    
    evenementImage = EvenementImage.objects.filter(evenement=evenement).order_by('id')[3:]
    nosPremiersPhotos = EvenementImage.objects.filter(evenement=evenement).order_by('-id')[:3]
    return render(request, 'admin/gestionEvenement/detailEvenement.html', 
                  {'evenement': evenement, 'evenementImage': evenementImage, 'nosPremiersPhotos':nosPremiersPhotos, 
                   'temoingnages': temoingnages})



def modifierEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    typeEvenement = TypeEvenement.objects.all()
    imageEvenement = EvenementImage.objects.filter(evenement=evenement)
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_evenement = request.POST.get('type_evenement')
        images = request.FILES.getlist('photos[]')
        evenementType = TypeEvenement.objects.get(pk=int(type_evenement))
        if images:
            photoCouverture = images[0]
            evenement.typeEvenement = evenementType
            # evenement.titre = titre
            evenement.photo = photoCouverture
            evenement.description = description
            evenement.save()
            # EvenementImage.objects.filter(evenement=evenement).delete()
            
          
            for image in range(0, len(images)):
                EvenementImage.objects.create(
                    evenement = evenement,
                    image = images[image]
                )
                return redirect('affichageEvenement')
        return redirect('affichageEvenement')
        
    return render(request, 'admin/gestionEvenement/modifierEvenement.html', {'evenement' : evenement, 'typeEvenem': typeEvenement, 'imageEvenements': imageEvenement})
    
def supprimerEvenement(request, id):
    evenement = Evenement.objects.get(id=id).delete()
    EvenementImage.objects.filter(evenement = evenement).delete()
    return redirect('affichageEvenement')


#-------------------------------------------GESTION TEMOIGNAGES----------------------------------

def listeTemoingnes(request):
    temoingnages = Temoingnage.objects.all()
    return render(request, 'admin/gestionEvenement/listeTemoingnes.html', {'temoingnages': temoingnages})


    
    
def ajoutTemoingnages(request):
    events = Evenement.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        image = request.FILES.get('image')
        message = request.POST.get('message')
        role = request.POST.get('role')
        evenement_id = request.POST.get('evenement')
        video = request.FILES.get('video')

        evenements = get_object_or_404(Evenement, id=evenement_id)

        Temoingnage.objects.create(
            nom=nom,
            image=image,
            message=message,
            role=role,
            evenement=evenements,
            video=video
        )

        return redirect(reverse('detailEvenements', kwargs={'id': evenements.id}) + '#temoingnages')

    return render(request, 'admin/gestionEvenement/ajoutTemoingnages.html', {'events': events})


def modifierTemoingnes(request, id):
    temoingnage = Temoingnage.objects.get(id=id)
    evenements = Evenement.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        image = request.FILES.get('image')
        message = request.POST.get('message')
        role = request.POST.get('role')
        evenement_id = request.POST.get('evenement')
        video = request.FILES.get('video')
        evenementsTemoigné = Evenement.objects.get(pk=int(evenement_id))
        temoingnage.nom = nom
        temoingnage.image = image
        temoingnage.message = message
        temoingnage.role = role
        temoingnage.evenement = evenementsTemoigné
        temoingnage.video = video
        temoingnage.save()
        return redirect('temoingnages')
    return render(request, 'admin/gestionEvenement/modifierTemoingnes.html', {'temoingnage': temoingnage, 'events': evenements})

def supprimerTemoingne(request, id):
    temoingnage = Temoingnage.objects.get(id=id)
    temoingnage.delete()
    return redirect('temoingnages')

# --------------------------------GESTION DES MEMBRES----------------------------------------

def liste_membres(request):
    # Récupérer la requête de recherche
    search_query = request.GET.get('search', '')
    
    # Filtrer les membres selon la recherche
    if search_query:
        membres = Membre.objects.filter(
            Q(nom__icontains=search_query) | 
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query)
        ).order_by('nom', 'prenom')
    else:
        membres = Membre.objects.all().order_by('nom', 'prenom')
    
    # Pagination (10 membres par page)
    paginator = Paginator(membres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/gestionMembre/liste.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })



def detail_membre(request, pk):
    membre = get_object_or_404(Membre, pk=pk)
    

    return render(request, 'admin/gestionMembre/detail.html', {
        'membre': membre
    })

def creer_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = MembreForm()
    
    return render(request, 'admin/gestionMembre/creer.html', {'form': form})

def modifier_membre(request, pk):
    membre = Membre.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():
            form.update(membre)
            return redirect('liste_membres')
    else:
        # Initialiser le formulaire avec les données du membre
        initial_data = {
            'nom': membre.nom,
            'prenom': membre.prenom,
            'sexe': membre.sexe,
            # ... tous les autres champs ...
        }
        form = MembreForm(initial=initial_data)
    
    return render(request, 'admin/gestionMembres/modifier.html', {'form': form, 'membre': membre})


#-----------------------------GESTION ANNONCES--------------------------------------------------


def liste_annonces(request):
    search_query = request.GET.get("search", "")

    if search_query:
        annonces = Annonce.objects.filter(titre__icontains=search_query).order_by('-date_creation')
    else:
        annonces = Annonce.objects.all().order_by('-date_creation')

    return render(request, 'admin/gestionAnnonce/liste.html', {'annonces': annonces})


# @login_required
def creer_annonce(request):
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user
            annonce.save()
            messages.success(request, "L'annonce a été mise à jour avec succès!")
            return redirect('liste_annonces')
    else:
        form = AnnonceForm()
    return render(request, 'admin/gestionAnnonce/creer.html', {'form': form})

# @login_required
def publier_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    annonce.est_publie = True
    annonce.date_publication = datetime.datetime.now()
    annonce.save()
    messages.success(request, "Annonce publiée avec succès")
    return redirect('liste_annonces')

def modifier_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user 
            
            # Si la case "Publier" est cochée, on met à jour la date de publication
            if form.cleaned_data['est_publie'] and not annonce.date_publication:
                annonce.date_publication = timezone.now()
            
            annonce.save()
            
            messages.success(request, "L'annonce a été mise à jour avec succès!")
            return redirect('liste_annonces')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AnnonceForm(instance=annonce)
    
    context = {
        'form': form,
        'annonce': annonce,
        'titre_page': 'Modifier Annonce',
        'btn_submit': 'Mettre à jour',
    }
    
    return render(request, 'admin/gestionAnnonce/modifier.html', context)


def supprimer_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    titre_annonce = annonce.titre
    annonce.delete()
    messages.success(request, f"L'annonce '{titre_annonce}' a été supprimée avec succès!")
    return redirect('liste_annonces')



#---------------------------------GESTION DES PAIEMENTS------------------------------------------

def liste_paiements(request):
    # Récupération des paramètres de filtrage
    event_id = request.GET.get("event_id")

    evenement = None

    paiements = Paiement.objects.all().order_by('-date_paiement')

    if event_id:
        paiements = paiements.filter(evenement__id= int(event_id))
        evenement = get_object_or_404(Evenement, id = event_id)

    evenement_id = request.GET.get('evenement')
    membre_id = request.GET.get('membre')
    
    
    
    if evenement_id:
        paiements = paiements.filter(evenement__id=evenement_id)
    if membre_id:
        paiements = paiements.filter(membre__id=membre_id)
    
    context = {
        'paiements': paiements,
        'membres': Membre.objects.all(),
        'evenements': Evenement.objects.all(),
        'selected_evenement': int(evenement_id) if evenement_id else None,
        'selected_membre': int(membre_id) if membre_id else None,
        'evenement': evenement,
    }
    return render(request, 'admin/gestionPaiement/liste.html', context)

def ajouter_paiement(request):
    evenements = Evenement.objects.all()
    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        if form.is_valid():
            paiement = form.save()
            messages.success(request, 'Paiement enregistré avec succès!')
            return redirect('liste_paiements')
    else:
        form = PaiementForm()
    
    
    
    return render(request, 'admin/gestionPaiement/ajouter.html',  {'form': form, 'evenements': evenements} )

def rappeler_paiements(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        # Récupérer les membres avec statut non payé ou moitié payé
        paiements = Paiement.objects.filter(evenement_id = event_id)
        
        # Préparer les emails
        email_messages = []
        for paiement in paiements:
            sujet = f"Rappel de paiement pour {paiement.evenement}"
            message = f"""
            Bonjour {paiement.membre.nom_complet},
            
            Nous vous rappelons que votre paiement pour l'événement {paiement.evenement}
            est toujours en statut {paiement.get_statut_display()}.
            
            Montant dû: {paiement.montant} €
            
            Merci de régulariser votre situation au plus vite.
            
            Cordialement,
            L'équipe d'administration
            """
            email_messages.append((
                sujet,
                message,
                'admin@example.com',
                [paiement.membre.email]
            ))
        
        # Envoyer les emails en masse
        send_mass_mail(email_messages, fail_silently=False)
        
        messages.success(request, f"Rappels envoyés !")
        return redirect('liste_paiements')
    
    return redirect('liste_paiements')