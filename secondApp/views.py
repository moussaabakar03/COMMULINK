from django.shortcuts import redirect, render

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Annee, Membre, Annonce, Paiement, EquipeDirigeante, Evenement, EvenementImage, Reinscription, Temoingnage, TypeEvenement, Utilisateur
from .forms import AnneeForm, MembreForm, AnnonceForm, PaiementForm, ReinscriptionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mass_mail
from time import timezone
import datetime
from django.db.models import Count
# from firtsApp.models import EquipeDirigeante, Evenement, EvenementImage, Temoingnage, TypeEvenement


from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


# DASHBOARD VIEW

def admin_dashboard(request):
    return render(request, "index.html")



#----------------------------------GESTION DES EVENEMENTS--------------------------------------

def listeCategorie(request):
    typeEvenement = TypeEvenement.objects.annotate(nombreEvenemnet=Count('evenement'))
    
    return render(request, 'gestionEvenement/listeCategorie.html', {
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
    return render(request, 'gestionEvenement/ajoutCategorie.html')

def modifierCategorie(request, id):
    categorie = get_object_or_404(TypeEvenement, pk=id)
    if request.method == 'POST':
        categorie.nom_type_evenement = request.POST.get('nom')
        categorie.image_type_evenement = request.FILES.get('photo')
        categorie.description_type_evenement = request.POST.get('description')
        categorie.save()

        return redirect('listeCategorie')
    return render(request, 'gestionEvenement/modifierCategorie.html', { 'categorie': categorie })

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
    return render(request, 'gestionEvenement/listeEvenement.html', {'evenements': evenements})

def ajoutEvenement(request):
    typeEvenem = TypeEvenement.objects.all()
    toutes_annees = Annee.objects.all()
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_evenement = request.POST.get('type_evenement')
        images = request.FILES.getlist('photos[]') 
        prix = request.POST.get("montant")
        annee_select = request.POST.get("annee")
        
        evenementType = TypeEvenement.objects.get(id=type_evenement)
        annee = Annee.objects.get(id=annee_select)
        
        if images:
            photoCouverture = images[0]
            evenement = Evenement.objects.create(
                typeEvenement= evenementType, photo=photoCouverture, description=description, prix = prix, titre = titre, annee = annee
            )
            
            for image in range(0, len(images)):
                EvenementImage.objects.create(
                    evenement = evenement,
                    image = images[image]
                )
        else:
            evenement = Evenement.objects.create(
                typeEvenement= evenementType, photo= None, description=description, prix = prix, titre = titre
            )
        return redirect('affichageEvenement')
    return render(request, 'gestionEvenement/ajoutEvenement.html', {'typeEvenem': typeEvenem, 'toutes_annees': toutes_annees})

def evenementFiltrer(request, id):
    categorieEvenemnt = TypeEvenement.objects.get(id = id)
    evenements = Evenement.objects.filter(typeEvenement__id=id)
    return render(request, "gestionEvenement/evenementFiltrer.html", {"evenements": evenements,"categorieEvenemnt": categorieEvenemnt})

def detailEvenements(request, id):
    evenement = Evenement.objects.get(id=id)
    
    temoingnages = Temoingnage.objects.filter(evenement = evenement)
    
    evenementImage = EvenementImage.objects.filter(evenement=evenement).order_by('id')[3:]
    nosPremiersPhotos = EvenementImage.objects.filter(evenement=evenement).order_by('-id')[:3]
    return render(request, 'gestionEvenement/detailEvenement.html', 
                  {'evenement': evenement, 'evenementImage': evenementImage, 'nosPremiersPhotos':nosPremiersPhotos, 
                   'temoingnages': temoingnages})



def modifierEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    typeEvenement = TypeEvenement.objects.all()
    toutes_annees = Annee.objects.all()
    imageEvenement = EvenementImage.objects.filter(evenement=evenement)
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_evenement = request.POST.get('type_evenement')
        anneeSelect = request.POST.get('annee')
        images = request.FILES.getlist('photos[]')
        prix = request.POST.get("prix")
        
        evenementType = TypeEvenement.objects.get(pk=int(type_evenement))
        annee = Annee.objects.get(pk=int(anneeSelect))
        
        evenement.typeEvenement = evenementType
        evenement.prix = prix
        evenement.description = description
        evenement.titre = titre
        evenement.annee = annee
        evenement.save()
        
        if images:
            photoCouverture = images[0]      
            evenement.photo = photoCouverture
                  
            evenement.save()
          
            for image in range(0, len(images)):
                EvenementImage.objects.create(
                    evenement = evenement,
                    image = images[image]
                )
                return redirect('affichageEvenement')
        return redirect('affichageEvenement')
        
    return render(request, 'gestionEvenement/modifierEvenement.html', {'evenement' : evenement, 'typeEvenem': typeEvenement, 'imageEvenements': imageEvenement, "toutes_annees": toutes_annees})
    
def supprimerEvenement(request, id):
    evenement = Evenement.objects.get(id=id).delete()
    EvenementImage.objects.filter(evenement = evenement).delete()
    return redirect('affichageEvenement')



def publier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    evenement.est_publie = True
    evenement.save()
    messages.success(request, "Evenement publié avec succès")
    return redirect('affichageEvenement')

def depublier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    evenement.est_publie = False
    evenement.save()
    messages.success(request, "Evenement dépublié avec succès")
    return redirect('affichageEvenement')

#-------------------------------------------GESTION TEMOIGNAGES----------------------------------

def listeTemoingnes(request):
    temoingnages = Temoingnage.objects.all()
    return render(request, 'gestionEvenement/listeTemoingnes.html', {'temoingnages': temoingnages})


    
    
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

    return render(request, 'gestionEvenement/ajoutTemoingnages.html', {'events': events})


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
    return render(request, 'gestionEvenement/modifierTemoingnes.html', {'temoingnage': temoingnage, 'events': evenements})

def supprimerTemoingne(request, id):
    temoingnage = Temoingnage.objects.get(id=id)
    temoingnage.delete()
    return redirect('temoingnages')


# --------------------------------GESTION DES MEMBRES----------------------------------------

def liste_membres(request):
    # Récupérer la requête de recherche
    search_query = request.GET.get('search', '').strip()
    
    nombreMembre = 0
    # Filtrer les membres selon la recherche
    if search_query:
        membres = Membre.objects.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(adresse__icontains=search_query) |
            Q(profession__icontains=search_query) |
            Q(niveauEtude__icontains=search_query) |
            Q(ecole__icontains=search_query) |
            Q(date_inscription__icontains=search_query) |
            Q(ner__icontains=search_query) |
            Q(keri__icontains=search_query) |
            Q(keribour__icontains=search_query) |
            Q(keriBa__icontains=search_query) |
            Q(keribourBa__icontains=search_query)
        ).order_by('nom', 'prenom')
        nombreMembre = membres.count()
    else:
        membres = Membre.objects.all().order_by('nom', 'prenom')
        nombreMembre = membres.count()
    
    # Pagination (10 membres par page)
    paginator = Paginator(membres, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gestionMembre/liste.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'nombreMembre': nombreMembre
    })

def detail_membre(request, pk):
    membre = get_object_or_404(Membre, pk=pk)
    

    return render(request, 'gestionMembre/detail.html', {
        'membre': membre
    })

# def creer_membre(request):
#     if request.method == 'POST':
#         form = MembreForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('liste_membres')
#     else:
#         form = MembreForm()
     
#     return render(request, 'gestionMembre/creer.html', {'form': form})

def creer_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Créer l'utilisateur
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data.get('telephone') or "defaultpass123"
            
            # Vérifier si l'email existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                form.add_error('email', 'Un utilisateur avec cet email existe déjà.')
                return render(request, 'gestionMembre/creer.html', {'form': form})
            
            utilisateur = Utilisateur.objects.create(
                username=email,
                email=email,
                password=make_password(telephone),
                first_name=nom,
                last_name=prenom,
                role="membreLambda",
                is_active=True,
            )
            
            # 2. Créer le membre
            membre = Membre(
                utilisateur=utilisateur,
                nom=nom,
                prenom=prenom,
                sexe=form.cleaned_data['sexe'],
                email=email,
                telephone=telephone,
                adresse=form.cleaned_data.get('adresse', ''),
                profession=form.cleaned_data['profession'],
                numeroUrgence=form.cleaned_data.get('numeroUrgence', ''),
                niveauEtude=form.cleaned_data.get('niveauEtude', ''),
                ecole=form.cleaned_data.get('ecole', ''),
                ner=form.cleaned_data.get('ner', ''),
                keri=form.cleaned_data.get('keri', ''),
                keribour=form.cleaned_data.get('keribour', ''),
                keriBa=form.cleaned_data.get('keriBa', ''),
                keribourBa=form.cleaned_data.get('keribourBa', ''),
                notes=form.cleaned_data.get('notes', ''),
            )
            
            # Gestion de la photo
            if form.cleaned_data.get('photo'):
                membre.photo = form.cleaned_data['photo']
            
            membre.save()

            # 3. Créer la réinscription pour l'année active
            annee_active = Annee.objects.order_by('-id').first()
            if annee_active:
                Reinscription.objects.create(
                    membre=membre,
                    annee=annee_active,
                    username=email,
                    password=telephone,
                    numeroUrgence=form.cleaned_data.get('numeroUrgence', ''),
                    ecole=form.cleaned_data.get('ecole', ''),
                    niveauEtude=form.cleaned_data.get('niveauEtude', ''),
                    photo_annuelle=form.cleaned_data.get('photo'),
                    filiere=form.cleaned_data.get('filiere', '')
                )

            messages.success(request, f'Le membre {nom} {prenom} a été créé avec succès.')
            return redirect('liste_membres')
    else:
        form = MembreForm()

    return render(request, 'gestionMembre/creer.html', {'form': form})


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
            'email': membre.email,
            'telephone': membre.telephone,
            'adresse': membre.adresse,
            'profession': membre.profession,
            'numeroUrgence': membre.numeroUrgence,
            'niveauEtude': membre.niveauEtude,
            'ecole': membre.ecole,
            'photo': membre.photo,
            'notes': membre.notes,
            'ner': membre.ner,
            'keri': membre.keri,
            'keribour': membre.keribour,
            'keriBa': membre.keriBa,
            'keribourBa': membre.keribourBa,
        }

        form = MembreForm(initial=initial_data)
    
    return render(request, 'gestionMembre/modifierMembre.html', {'form': form, 'membre': membre})

def supprimer_membre(request, pk):
    membre = Membre.objects.get(pk=pk).delete()
    messages.success(request, "Membre supprimé avec succès!")
    return redirect('liste_membres')
    
    

def liste_EquipeDirigeante(request):
    # Récupérer la requête de recherche
    search_query = request.GET.get('search', '').strip()
    
    # Filtrer les membres selon la recherche
    if search_query:
        membres = EquipeDirigeante.objects.filter(
            Q(nom__icontains=search_query) | 
            Q(role__icontains=search_query) |
            Q(lienFacebook__icontains=search_query) |
            Q(lienTwitter__icontains=search_query) |
            Q(lienInstagram__icontains=search_query)
        ).order_by('nom')
    else:
        membres = EquipeDirigeante.objects.all().order_by('nom')
    
    # Pagination (10 membres par page)
    paginator = Paginator(membres, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gestionMembre/listeMembreEquipe.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def ajoutMembreEquipe(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')
        role = request.POST.get('role')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        
        utilisateur = Utilisateur.objects.create(
            username = role,
            password = make_password(role),
            role="membreEquipe",
            is_active=True,
            is_staff = True
        )
        
        EquipeDirigeante.objects.create(
            utilisateur = utilisateur, nom = nom, image = photo, role = role, lienFacebook = facebook, lienInstagram = instagram , lienTwitter = twitter
        )
        return redirect("liste_EquipeDirigeante")
    return render(request, 'gestionMembre/ajoutMembreEquipe.html')

def modification_MembreEquipeDirigeante(request, pk):
    # Récupérer le membre à modifier ou retourner 404 si non trouvé
    membre = get_object_or_404(EquipeDirigeante, pk=pk)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        role = request.POST.get('role')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        photo = request.FILES.get('photo')
        
        # Mettre à jour les champs
        membre.nom = nom
        membre.role = role
        membre.lienFacebook = facebook
        membre.lienInstagram = instagram
        membre.lienTwitter = twitter
        
        # Mettre à jour la photo seulement si une nouvelle est fournie
        if photo:
            membre.image = photo
        
        # Sauvegarder les modifications
        membre.save()
        
        # Message de succès (optionnel)
        messages.success(request, 'Membre modifié avec succès!')
        
        # Rediriger vers la liste
        return redirect("liste_EquipeDirigeante")
    
    # Passer le membre au template pour pré-remplir le formulaire
    context = {
        'membre': membre
    }
    
    return render(request, 'gestionMembre/modifierMembreEquipe.html', context)


def supprimer_MembreEquipe(request, pk):
    membre = get_object_or_404(EquipeDirigeante, pk=pk).delete()
    return redirect("liste_EquipeDirigeante")



#-----------------------------GESTION ANNONCES--------------------------------------------------


def liste_annonces(request):
    search_query = request.GET.get("search", "")

    if search_query:
        annonces = Annonce.objects.filter(titre__icontains=search_query).order_by('-date_creation')
    else:
        annonces = Annonce.objects.all().order_by('-date_creation')

    return render(request, 'gestionAnnonce/liste.html', {'annonces': annonces})


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
    return render(request, 'gestionAnnonce/creer.html', {'form': form})

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
            # if form.cleaned_data['est_publie'] and not annonce.date_publication:
            #     annonce.date_publication = timezone.now()
            
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
    
    return render(request, 'gestionAnnonce/modifier.html', context)

def supprimer_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    titre_annonce = annonce.titre
    annonce.delete()
    messages.success(request, f"L'annonce '{titre_annonce}' a été supprimée avec succès!")
    return redirect('liste_annonces')


#---------------------------------GESTION DES ANNEES------------------------------------------

def listeAnnee(request):
    annees = Annee.objects.all()

    context = {
        'annees': annees,
    }
    return render(request, "gestionAnnee/listeAnnee.html", context)

def ajoutAnnee(request):
     
    if request.method == 'POST':
        form = AnneeForm(request.POST)
        
        if form.is_valid():
            debutAnnee = form.cleaned_data['debutAnnee']
            finAnnee = form.cleaned_data['finAnnee']

            Annee.objects.create(
                debutAnnee = debutAnnee,
                finAnnee = finAnnee
            )
            
            messages.success(request, 'Nouvelle année enregistré avec succès !')
            return redirect('listeAnnee')

    else:
        form = AnneeForm()
        
    return render(request, "gestionAnnee/ajoutAnnee.html",  {
        'form': form,
    })


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
    return render(request, 'gestionPaiement/liste.html', context)

def ajouter_paiement(request):
    evenements = Evenement.objects.all()
    
    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        
        if form.is_valid():
            montant = form.cleaned_data['montant']
            evenement = form.cleaned_data['evenement']
            membre = form.cleaned_data['membre']
            date_paiement = form.cleaned_data['date_paiement']
            preuve_paiement = form.cleaned_data.get('preuve_paiement')

            paiement_existant = Paiement.objects.filter(
                membre=membre,
                evenement=evenement
            ).first()

            # --- Si le paiement existe déjà, on met à jour ---
            if paiement_existant:
                paiement_existant.montant += montant
                paiement_existant.date_paiement = date_paiement or paiement_existant.date_paiement
                if preuve_paiement:
                    paiement_existant.preuve_paiement = preuve_paiement

                # --- Déterminer le statut selon le montant cumulé ---
                prix = paiement_existant.evenement.prix
                montant_total = paiement_existant.montant

                if montant_total >= prix:
                    paiement_existant.statut = "payé"
                elif montant_total >= (prix / 2):
                    paiement_existant.statut = "moitié_payé"
                elif montant_total > 0:
                    paiement_existant.statut = "avance"
                else:
                    paiement_existant.statut = "non_payé"

                paiement_existant.save()
                messages.success(request, 'Paiement mis à jour avec succès !')
                return redirect('liste_paiements')

            # --- Sinon, créer un nouveau paiement ---
            else:
                paiement = form.save(commit=False)
                prix = evenement.prix

                if montant >= prix:
                    paiement.statut = "payé"
                elif montant >= (prix / 2):
                    paiement.statut = "moitié_payé"
                elif montant > 0:
                    paiement.statut = "avance"
                else:
                    paiement.statut = "non_payé"

                paiement.save()
                messages.success(request, 'Nouveau paiement enregistré avec succès !')
                return redirect('liste_paiements')
    
    else:
        form = PaiementForm()
    
    return render(request, 'gestionPaiement/ajouter.html', {
        'form': form,
        'evenements': evenements
    })


def rappeler_paiements(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if not event_id:
            messages.error(request, "Aucun événement sélectionné.")
            return redirect('liste_paiements')

        # 🔹 Récupérer les paiements partiels ou non payés
        paiements = Paiement.objects.filter(
            evenement_id=event_id,
            statut__in=['non_payé', 'moitié_payé', 'avance']
        )

        if not paiements.exists():
            messages.info(request, "Aucun membre à relancer pour cet événement.")
            return redirect('liste_paiements')

        # 🔹 Préparer les emails
        email_messages = []
        for paiement in paiements:
            montant_du = paiement.evenement.prix - paiement.montant

            sujet = f"Rappel de paiement - {paiement.evenement.titre}"
            message = f"""
                Bonjour {paiement.membre.nom_complet},

                Nous vous rappelons que votre paiement pour l'événement **{paiement.evenement.titre}** 
                est actuellement en statut **{paiement.get_statut_display()}**.

                Montant payé : {paiement.montant} Fcfa  
                Montant total : {paiement.evenement.prix} Fcfa  
                Montant restant : {montant_du} Fcfa

                Merci de bien vouloir régulariser votre paiement dans les plus brefs délais.

                Cordialement,  
                L’équipe d’administration
                """

            # Vérifier que l’email du membre existe
            if paiement.membre.email:
                email_messages.append((
                    sujet,
                    message,
                    'admin@example.com',  # ✅ à remplacer par ton email d’administration réel
                    [paiement.membre.email]
                ))

        # 🔹 Envoi des emails
        if email_messages:
            send_mass_mail(email_messages, fail_silently=False)
            messages.success(request, f"Rappels envoyés à {len(email_messages)} membre(s).")
        else:
            messages.warning(request, "Aucun membre avec une adresse e-mail valide.")

        return redirect('liste_paiements')

    return redirect('liste_paiements')


def modifierPaiement(request, pk):
    # Récupérer le paiement à modifier ou retourner 404 si non trouvé
    paiement = get_object_or_404(Paiement, pk=pk)
    evenements = Evenement.objects.all()
    
    if request.method == 'POST':
        # Passer l'instance existante au formulaire pour la mise à jour
        form = PaiementForm(request.POST, request.FILES, instance=paiement)
        if form.is_valid():
            
            montant = form.cleaned_data['montant']
            evenement = form.cleaned_data['evenement']
            
            # Détermination du statut
            if montant >= evenement.prix:
                statut = "payé"
            elif montant >= (evenement.prix / 2):
                statut = "moitié_payé"
            elif montant < (evenement.prix / 2):
                statut = "avance"
            else:
                statut = "non_payé"
            
            # Enregistrement du paiement
            paiement = form.save(commit=False)
            paiement.statut = statut
            paiement.save()
            
            form.save()
            messages.success(request, 'Paiement modifié avec succès!')
            return redirect('liste_paiements')
        else:
            messages.error(request, 'Erreur lors de la modification. Veuillez vérifier les champs.')
    else:
        # Pré-remplir le formulaire avec les données existantes
        form = PaiementForm(instance=paiement)
    
    context = {
        'form': form,
        'evenements': evenements,
        'paiement': paiement
    }
    
    return render(request, 'gestionPaiement/modifierPaiment.html', context)


def paiementParEvenement(request, pk):
    evenement = get_object_or_404(Evenement, id = pk)
    
    paiements = Paiement.objects.filter(evenement = evenement).order_by('-date_paiement')
    
    membre_id = request.GET.get('membre')
    if membre_id:
        paiements = paiements.filter(membre__id=membre_id)
    
    
    contexte = {"paiements": paiements, "evenement": evenement, 'membres': Membre.objects.all(),}
    return render(request, "gestionPaiement/paiementParEvenement.html", contexte)



def reinscriptionUser(request):
    if request.method == 'POST':
        form = ReinscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if not user:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
                return render(request, "gestionMembre/reinscriptionUser.html", {'form': form})

            try:
                membre = Membre.objects.get(utilisateur=user)
            except Membre.DoesNotExist:
                messages.error(request, "Aucun membre associé à cet utilisateur.")
                return render(request, "gestionMembre/reinscriptionUser.html", {'form': form})

            annee_active = Annee.objects.order_by('-id').first()
            if not annee_active:
                messages.error(request, "Aucune année active trouvée.")
                return render(request, "gestionMembre/reinscriptionUser.html", {'form': form})

            if Reinscription.objects.filter(membre=membre, annee=annee_active).exists():
                messages.warning(request, "Vous êtes déjà réinscrit pour cette année.")
                return redirect("index")

            Reinscription.objects.create(
                membre=membre,
                annee=annee_active,
                numeroUrgence=form.cleaned_data.get('numeroUrgence'),
                adresse=form.cleaned_data.get('adresse'),
                ecole=form.cleaned_data.get('ecole'),
                niveauEtude=form.cleaned_data.get('niveauEtude'),
                filiere=form.cleaned_data.get('filiere'),
                photo_annuelle=form.cleaned_data.get('photo_annuelle')
            )

            messages.success(request, "Votre réinscription a été effectuée avec succès!")
            return redirect("index")
    else:
        form = ReinscriptionForm()

    return render(request, "gestionMembre/reinscriptionUser.html", {'form': form})





