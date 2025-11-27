from django.shortcuts import redirect, render


from django.http import HttpResponseRedirect
from django.urls import reverse

from commulink.utils.decorators import admin_required
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

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, "index.html")



#----------------------------------GESTION DES EVENEMENTS--------------------------------------

@login_required
@admin_required
def listeCategorie(request):
    typeEvenement = TypeEvenement.objects.annotate(nombreEvenemnet=Count('evenement'))
    
    return render(request, 'gestionEvenement/listeCategorie.html', {
        'typeEvenement': typeEvenement
    })



@login_required
@admin_required
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


@login_required
@admin_required
def modifierCategorie(request, id):
    categorie = get_object_or_404(TypeEvenement, pk=id)
    if request.method == 'POST':
        categorie.nom_type_evenement = request.POST.get('nom')
        categorie.image_type_evenement = request.FILES.get('photo')
        categorie.description_type_evenement = request.POST.get('description')
        categorie.save()

        return redirect('listeCategorie')
    return render(request, 'gestionEvenement/modifierCategorie.html', { 'categorie': categorie })



@login_required
@admin_required
def supprimerCategorie(request, id):
    categorie = get_object_or_404(TypeEvenement, pk=id)
    categorie.delete()
    return redirect('listeCategorie')

# def affichageEvenement(request, id):
#     evenement = TypeEvenement.objects.get(id = id)
#     evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
#     return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})


@login_required
@admin_required
def affichageEvenement(request):
    evenements = Evenement.objects.all().order_by('-id')
    return render(request, 'gestionEvenement/listeEvenement.html', {'evenements': evenements})

@login_required
@admin_required
def ajoutEvenement(request):
    typeEvenem = TypeEvenement.objects.all()
    toutes_annees = Annee.objects.all().order_by("-id")
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

@login_required
@admin_required
def evenementFiltrer(request, id):
    categorieEvenemnt = TypeEvenement.objects.get(id = id)
    evenements = Evenement.objects.filter(typeEvenement__id=id)
    return render(request, "gestionEvenement/evenementFiltrer.html", {"evenements": evenements,"categorieEvenemnt": categorieEvenemnt})

@login_required
@admin_required
def detailEvenements(request, id):
    evenement = Evenement.objects.get(id=id)
    
    temoingnages = Temoingnage.objects.filter(evenement = evenement)
    
    evenementImage = EvenementImage.objects.filter(evenement=evenement).order_by('id')[3:]
    nosPremiersPhotos = EvenementImage.objects.filter(evenement=evenement).order_by('-id')[:3]
    return render(request, 'gestionEvenement/detailEvenement.html', 
                  {'evenement': evenement, 'evenementImage': evenementImage, 'nosPremiersPhotos':nosPremiersPhotos, 
                   'temoingnages': temoingnages})



@login_required
@admin_required
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


@login_required
@admin_required    
def supprimerEvenement(request, id):
    evenement = Evenement.objects.get(id=id).delete()
    EvenementImage.objects.filter(evenement = evenement).delete()
    return redirect('affichageEvenement')



@login_required
@admin_required
def publier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    evenement.est_publie = True
    evenement.save()
    messages.success(request, "Evenement publié avec succès")
    return redirect('affichageEvenement')


@login_required
@admin_required
def depublier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    evenement.est_publie = False
    evenement.save()
    messages.success(request, "Evenement dépublié avec succès")
    return redirect('affichageEvenement')

#-------------------------------------------GESTION TEMOIGNAGES----------------------------------


@login_required
@admin_required
def listeTemoingnes(request):
    temoingnages = Temoingnage.objects.all()
    return render(request, 'gestionEvenement/listeTemoingnes.html', {'temoingnages': temoingnages})


    

@login_required
@admin_required    
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


@login_required
@admin_required
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

@login_required
@admin_required
def supprimerTemoingne(request, id):
    temoingnage = Temoingnage.objects.get(id=id)
    temoingnage.delete()
    return redirect('temoingnages')


# --------------------------------GESTION DES MEMBRES----------------------------------------

@login_required
@admin_required
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
            Q(telephone__icontains=search_query) |
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
    paginator = Paginator(membres, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gestionMembre/liste.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'nombreMembre': nombreMembre
    })

@login_required
@admin_required
def detail_membre(request, pk):
    membre = get_object_or_404(Membre, pk=pk)
    
    reinscriptionMembres = membre.reinscriptions.all()

    return render(request, 'gestionMembre/detail.html', {
        'membre': membre,
        "reinscriptionMembres": reinscriptionMembres
    })


@login_required
@admin_required
def creer_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():

            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data.get('telephone') or "defaultpass123"
            
            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, 'Un utilisateur avec cet email existe déjà.')
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
                    adresse=form.cleaned_data.get('adresse', ''),
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


@login_required
@admin_required
def modidfier_membre(request, pk):
    membre = Membre.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():
            
            
            email = form.cleaned_data['email']
            telephone = form.cleaned_data.get('telephone') or "defaultpass123"
            
            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, 'Un utilisateur avec cet email existe déjà.')
                return render(request, 'gestionMembre/modifierMembre.html', {'form': form, 'membre': membre})
            
            
            membre.utilisateur.username = email
            membre.utilisateur.password=make_password(telephone),

            form.update(membre)
            messages.success(request, "Membre modifié avec succès!")
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


@login_required
@admin_required
def modifier_membre(request, pk):
    membre = Membre.objects.get(pk=pk)
    utilisateur = membre.utilisateur

    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email']
            telephone = form.cleaned_data.get('telephone') or "defaultpass123"

            # Vérifier doublon email sans compter le compte actuel
            if Utilisateur.objects.filter(email=email).exclude(pk=utilisateur.pk).exists():
                messages.error(request, 'Un utilisateur avec cet email existe déjà.')
                return render(request, 'gestionMembre/modifierMembre.html', {'form': form, 'membre': membre})

            # Mettre à jour le compte utilisateur
            utilisateur.username = email
            utilisateur.email = email
            utilisateur.password = make_password(telephone)
            utilisateur.save()

            # Mettre à jour le membre
            form.update(membre)

            messages.success(request, "Membre modifié avec succès!")
            return redirect('liste_membres')

    else:
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



@login_required
@admin_required
def supprimer_membre(request, pk):
    membre = Membre.objects.get(pk=pk).delete()
    messages.success(request, "Membre supprimé avec succès!")
    return redirect('liste_membres')
    

from django.core.paginator import Paginator
from django.db.models import Q
from .models import Reinscription, Annee

# def listess_reinscriptions(request):
#     """
#     Vue pour afficher la liste des réinscriptions avec recherche et filtres
#     """
#     # Récupérer tous les réinscriptions
#     reinscriptions = Reinscription.objects.select_related('membre', 'annee').all()
    
#     # ========== RECHERCHE ==========
#     search_query = request.GET.get('search', '').strip()
#     if search_query:
#         reinscriptions = reinscriptions.filter(
#             Q(membre__nom_complet__icontains=search_query) |
#             Q(membre__nom__icontains=search_query) |
#             Q(membre__prenom__icontains=search_query) |
#             Q(ecole__icontains=search_query) |
#             Q(filiere__icontains=search_query) |
#             Q(niveauEtude__icontains=search_query) |
#             Q(membre__ner__icontains=search_query) |
#             Q(membre__keri__icontains=search_query)
#         )
    
#     # ========== FILTRES ==========
#     # Filtre par année
#     annee_filter = request.GET.get('annee', '').strip()
#     if annee_filter:
#         reinscriptions = reinscriptions.filter(annee_id=annee_filter)
    
#     # Filtre par école
#     ecole_filter = request.GET.get('ecole', '').strip()
#     if ecole_filter:
#         reinscriptions = reinscriptions.filter(ecole=ecole_filter)
    
#     # Filtre par niveau
#     niveau_filter = request.GET.get('niveau', '').strip()
#     if niveau_filter:
#         reinscriptions = reinscriptions.filter(niveauEtude=niveau_filter)
    
#     # ========== DONNÉES POUR LES FILTRES ==========
#     # Liste des années disponibles
#     annees = Annee.objects.all().order_by('-id')
    
#     # Liste des écoles uniques (sans doublons et sans valeurs nulles)
#     ecoles = Reinscription.objects.exclude(
#         ecole__isnull=True
#     ).exclude(
#         ecole__exact=''
#     ).values_list('ecole', flat=True).distinct().order_by('ecole')
    
#     # Liste des niveaux uniques
#     niveaux = Reinscription.objects.exclude(
#         niveauEtude__isnull=True
#     ).exclude(
#         niveauEtude__exact=''
#     ).values_list('niveauEtude', flat=True).distinct().order_by('niveauEtude')
    
#     # ========== STATISTIQUES ==========
#     nombreReinscriptions = reinscriptions.count()
    
#     # ========== TRI ==========
#     # Trier par date de réinscription (les plus récentes en premier)
#     reinscriptions = reinscriptions.order_by('-date_reinscription')
    
#     # ========== PAGINATION ==========
    
#     paginator = Paginator(reinscriptions, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     # ========== CONTEXTE ==========
#     context = {
#         'page_obj': page_obj,
#         'nombreReinscriptions': nombreReinscriptions,
#         'search_query': search_query,
#         'annees': annees,
#         'ecoles': ecoles,
#         'niveaux': niveaux,
#         'annee_filter': annee_filter,
#         'ecole_filter': ecole_filter,
#         'niveau_filter': niveau_filter,
#     }
    
#     return render(request, 'gestionMembre/listeReinscription.html', context)




from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Reinscription, Annee

@login_required
@admin_required
def liste_reinscriptions(request):
    # Récupérer tous les paramètres de filtrage
    search_query = request.GET.get('search', '').strip()
    annee_id = request.GET.get('annee', '').strip()
    ecole_filter = request.GET.get('ecole', '').strip()
    niveau_filter = request.GET.get('niveau', '').strip()
    filiere_filter = request.GET.get('filiere', '').strip()

    total_reinscris = Reinscription.objects.all().count()
    # Récupérer toutes les réinscriptions avec les relations
    reinscriptions = Reinscription.objects.select_related('membre', 'annee').all().order_by('-date_reinscription')

    from django.db.models import Value, CharField
    from django.db.models.functions import Concat
    from django.db.models import Q

    reinscriptions = reinscriptions.annotate(
        nom_complet=Concat(
            'membre__nom', Value(' '), 'membre__prenom',
            output_field=CharField()
        )
    )
    # Appliquer les filtres
    if search_query:
        reinscriptions = reinscriptions.filter(
            Q(nom_complet__icontains=search_query) |
            Q(membre__nom__icontains=search_query) |
            Q(membre__prenom__icontains=search_query) |
            Q(ecole__icontains=search_query) |
            Q(filiere__icontains=search_query) |
            Q(niveauEtude__icontains=search_query) |
            Q(membre__ner__icontains=search_query) |
            Q(membre__keri__icontains=search_query)
        )

    if annee_id:
        reinscriptions = reinscriptions.filter(annee_id=annee_id)

    if ecole_filter:
        reinscriptions = reinscriptions.filter(ecole=ecole_filter)

    if niveau_filter:
        reinscriptions = reinscriptions.filter(niveauEtude=niveau_filter)

    if filiere_filter:
        reinscriptions = reinscriptions.filter(filiere=filiere_filter)

    # Calculer les statistiques
    total_reinscriptions = reinscriptions.count()
    
    # Réinscriptions de cette année
    debut_annee = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    annee_actuelle = Annee.objects.last()
    reinscriptions_cette_annee = Reinscription.objects.filter(annee=annee_actuelle).count()
    
    # Réinscriptions du dernier mois
    il_y_a_un_mois = timezone.now() - timedelta(days=30)
    reinscriptions_dernier_mois = Reinscription.objects.filter(
        date_reinscription__gte=il_y_a_un_mois
    ).count()

    # Préparer les données pour les filtres
    annees = Annee.objects.all().order_by('-debutAnnee')  # Supposons que le modèle Annee a un champ 'nom'
    
    # Récupérer les valeurs distinctes pour les filtres
    ecoles = Reinscription.objects.exclude(ecole__isnull=True).exclude(ecole__exact='').values_list('ecole', flat=True).distinct().order_by('ecole')
    niveaux = Reinscription.objects.exclude(niveauEtude__isnull=True).exclude(niveauEtude__exact='').values_list('niveauEtude', flat=True).distinct().order_by('niveauEtude')
    filieres = Reinscription.objects.exclude(filiere__isnull=True).exclude(filiere__exact='').values_list('filiere', flat=True).distinct().order_by('filiere')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(reinscriptions, 5)  # 20 réinscriptions par page
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'total_reinscris': total_reinscris,
        'nombreReinscription': total_reinscriptions,
        'search_query': search_query,
        'stats': {
            'total': total_reinscriptions,
            'cette_annee': reinscriptions_cette_annee,
            'dernier_mois': reinscriptions_dernier_mois,
        },
        'annees': annees,
        'annee_selectionnee': annee_id,
        'ecoles': ecoles,
        'ecole_selectionnee': ecole_filter,
        'niveaux': niveaux,
        'niveau_selectionne': niveau_filter,
        'filieres': filieres,
        'filiere_selectionnee': filiere_filter,
    }

    return render(request, 'gestionMembre/listeReinscription.html', context)



@login_required
@admin_required
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
    paginator = Paginator(membres, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gestionMembre/listeMembreEquipe.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

@login_required
@admin_required
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

@login_required
@admin_required
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


@login_required
@admin_required
def supprimer_MembreEquipe(request, pk):
    membre = get_object_or_404(EquipeDirigeante, pk=pk).delete()
    return redirect("liste_EquipeDirigeante")



#-----------------------------GESTION ANNONCES--------------------------------------------------


@login_required
@admin_required
def liste_annonces(request):
    search_query = request.GET.get("search", "")

    if search_query:
        annonces = Annonce.objects.filter(titre__icontains=search_query).order_by('-date_creation')
    else:
        annonces = Annonce.objects.all().order_by('-date_creation')

    return render(request, 'gestionAnnonce/liste.html', {'annonces': annonces})



@login_required
@admin_required
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


@login_required
@admin_required
def publier_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    annonce.est_publie = True
    annonce.date_publication = datetime.datetime.now()
    annonce.save()
    messages.success(request, "Annonce publiée avec succès")
    return redirect('liste_annonces')

@login_required
@admin_required
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

@login_required
@admin_required
def supprimer_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    titre_annonce = annonce.titre
    annonce.delete()
    messages.success(request, f"L'annonce '{titre_annonce}' a été supprimée avec succès!")
    return redirect('liste_annonces')


#---------------------------------GESTION DES ANNEES------------------------------------------

@login_required
@admin_required
def listeAnnee(request):
    annees = Annee.objects.all().order_by("id")

    context = {
        'annees': annees,
    }
    return render(request, "gestionAnnee/listeAnnee.html", context)

@login_required
@admin_required
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

@login_required
@admin_required
def modifierAnnee(request, pk):
    annee = get_object_or_404(Annee, pk=pk)
    form = AnneeForm()
    if request.method == "POST":
        form = AnneeForm(request.POST)
        
        if form.is_valid():
            annee.debutAnnee = form.cleaned_data['debutAnnee']
            annee.finAnnee = form.cleaned_data['finAnnee']
            
            annee.save()
            
            messages.success(request, "Année modifiée avec succès!")
            return redirect("listeAnnee")
    else:
        form = AnneeForm(initial = {"debutAnnee": annee.debutAnnee, "finAnnee": annee.finAnnee})
    context = {"form": form, "annee": annee}
    return render(request, "gestionAnnee/modifierAnnee.html", context)

#---------------------------------GESTION DES PAIEMENTS------------------------------------------

@login_required
@admin_required
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
        paiements = paiements.filter(membre_Reinscris__membre__id=membre_id)
    
    context = {
        'paiements': paiements,
        'membres': Membre.objects.all(),
        'evenements': Evenement.objects.all(),
        'selected_evenement': int(evenement_id) if evenement_id else None,
        'selected_membre': int(membre_id) if membre_id else None,
        'evenement': evenement,
    }
    return render(request, 'gestionPaiement/liste.html', context)

@login_required
@admin_required
def ajouter_paiement(request):
    evenements = Evenement.objects.all()
    
    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        
        if form.is_valid():
            montant = form.cleaned_data['montant']
            evenement = form.cleaned_data['evenement']
            membre_Reinscris = form.cleaned_data['membre_Reinscris']
            date_paiement = form.cleaned_data['date_paiement']
            preuve_paiement = form.cleaned_data.get('preuve_paiement')

            paiement_existant = Paiement.objects.filter(
                membre_Reinscris=membre_Reinscris,
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

@login_required
@admin_required
def ajoutPaiementEvenement(request, pk):
    evenement = get_object_or_404(Evenement, id=pk)

    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            membre_Reinscris = form.cleaned_data['membre_Reinscris']
            date_paiement = form.cleaned_data['date_paiement']
            preuve_paiement = form.cleaned_data.get('preuve_paiement')

            paiement_existant = Paiement.objects.filter(
                membre_Reinscris=membre_Reinscris,
                evenement=evenement
            ).first()

            if paiement_existant:
                paiement_existant.montant += montant
                paiement_existant.date_paiement = date_paiement or paiement_existant.date_paiement
                if preuve_paiement:
                    paiement_existant.preuve_paiement = preuve_paiement

                prix = evenement.prix
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
                return redirect('paiementParEvenement', pk=pk)

            else:
                paiement = form.save(commit=False)
                paiement.evenement = evenement   
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
                return redirect('paiementParEvenement', pk=pk)
        else:
            messages.error(request, "Erreur : formulaire non valide")
    else:
        form = PaiementForm()

    return render(request, "gestionPaiement/ajoutPaiementEvenement.html", {
        'form': form,
        'evenement': evenement
    })


@login_required
@admin_required
def rappeler_paiements(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if not event_id:
            messages.error(request, "Aucun événement sélectionné.")
            return redirect('liste_paiements')

        evenement = get_object_or_404(Evenement, id=event_id)
        
        # Récupérer tous les cas
        paiements_existants = Paiement.objects.filter(
            evenement_id=event_id,
            statut__in=['non_payé', 'moitié_payé', 'avance']
        )
        
        membres_ayant_paye = paiements_existants.values_list('membre_Reinscris_id', flat=True)
        
        reinscriptions_sans_paiement = Reinscription.objects.filter(
            annee=evenement.annee
        ).exclude(id__in=membres_ayant_paye)

        email_messages = []
        compteurs = {
            'non_payes': 0,
            'partiels': 0,
            'sans_paiement': 0
        }

        # Cas 1: Paiements existants
        for paiement in paiements_existants:
            montant_du = paiement.evenement.prix - paiement.montant

            sujet = f"Rappel de paiement - {paiement.evenement.titre}"
            message = f"""Bonjour {paiement.membre_Reinscris.membre.nom_complet},

Nous vous rappelons que votre paiement pour l'événement **{paiement.evenement.titre}** 
est actuellement en statut **{paiement.get_statut_display()}**.

Montant payé : {paiement.montant} Fcfa  
Montant total : {paiement.evenement.prix} Fcfa  
Montant restant : {montant_du} Fcfa

Merci de bien vouloir régulariser votre paiement dans les plus brefs délais.

Cordialement,  
L'équipe d'administration"""

            if paiement.membre_Reinscris.membre.email:
                email_messages.append((
                    sujet,
                    message.strip(),
                    'admin@example.com', 
                    [paiement.membre_Reinscris.membre.email]
                ))
                
                # Compter par statut
                if paiement.statut == 'non_payé':
                    compteurs['non_payes'] += 1
                else:
                    compteurs['partiels'] += 1

        # Cas 2: Membres sans paiement
        for reinscription in reinscriptions_sans_paiement:
            sujet = f"Rappel de paiement - {evenement.titre}"
            message = f"""Bonjour {reinscription.membre.nom_complet},

Nous vous rappelons que vous n'avez pas encore effectué de paiement pour l'événement **{evenement.titre}**.

Montant total à payer : {evenement.prix} Fcfa  
Statut : Non payé

Merci de bien vouloir effectuer votre paiement dans les plus brefs délais.

Cordialement,  
L'équipe d'administration"""

            if reinscription.membre.email:
                email_messages.append((
                    sujet,
                    message.strip(),
                    'admin@example.com', 
                    [reinscription.membre.email]
                ))
                compteurs['sans_paiement'] += 1

        # Envoi des emails
        if email_messages:
            try:
                send_mass_mail(email_messages, fail_silently=False)
                messages.success(request, 
                    f"Rappels envoyés à {len(email_messages)} membre(s): "
                    f"{compteurs['non_payes']} non payés, "
                    f"{compteurs['partiels']} partiellement payés, "
                    f"{compteurs['sans_paiement']} sans paiement."
                )
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi des emails: {str(e)}")
        else:
            messages.warning(request, "Aucun membre avec une adresse e-mail valide à rappeler.")

        return redirect('paiementParEvenement', pk=event_id)

    return redirect('liste_paiements')



# def rappeler_paiements(request):
#     if request.method == 'POST':
#         event_id = request.POST.get('event_id')
#         if not event_id:
#             messages.error(request, "Aucun événement sélectionné.")
#             return redirect('liste_paiements')

#         # 🔹 Récupérer les paiements partiels ou non payés
#         paiements = Paiement.objects.filter(
#             evenement_id=event_id,
#             statut__in=['non_payé', 'moitié_payé', 'avance']
#         )

#         if not paiements.exists():
#             messages.info(request, "Aucun membre à relancer pour cet événement.")
#             return redirect('liste_paiements')

#         # 🔹 Préparer les emails
#         email_messages = []
#         for paiement in paiements:
#             montant_du = paiement.evenement.prix - paiement.montant

#             sujet = f"Rappel de paiement - {paiement.evenement.titre}"
#             message = f"""
#                 Bonjour {paiement.membre.nom_complet},

#                 Nous vous rappelons que votre paiement pour l'événement **{paiement.evenement.titre}** 
#                 est actuellement en statut **{paiement.get_statut_display()}**.

#                 Montant payé : {paiement.montant} Fcfa  
#                 Montant total : {paiement.evenement.prix} Fcfa  
#                 Montant restant : {montant_du} Fcfa

#                 Merci de bien vouloir régulariser votre paiement dans les plus brefs délais.

#                 Cordialement,  
#                 L’équipe d’administration
#                 """

#             # Vérifier que l’email du membre existe
#             if paiement.membre.email:
#                 email_messages.append((
#                     sujet,
#                     message,
#                     'admin@example.com', 
#                     [paiement.membre.email]
#                 ))

#         # 🔹 Envoi des emails
#         if email_messages:
#             send_mass_mail(email_messages, fail_silently=False)
#             messages.success(request, f"Rappels envoyés à {len(email_messages)} membre(s).")
#         else:
#             messages.warning(request, "Aucun membre avec une adresse e-mail valide.")

#         return redirect('liste_paiements')

#     return redirect('liste_paiements')





@login_required
@admin_required 
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


@login_required
@admin_required
def paiementParEvenement(request, pk):
    evenement = get_object_or_404(Evenement, id = pk)
    
    paiements = Paiement.objects.filter(evenement = evenement).order_by('-date_paiement')
    
    # 2. Récupérer les IDs des membres déjà réinscrits et ayant fait un paiement
    membres_ayant_paye = paiements.values_list('membre_Reinscris_id', flat=True)

    # 3. Trouver les réinscriptions de l'année en excluant ceux qui ont payé
    reinscris = Reinscription.objects.filter(annee=evenement.annee).exclude(id__in=membres_ayant_paye)

    
    membre_id = request.GET.get('membreReinscris_id')
    if membre_id:
        paiements = paiements.filter(membre_Reinscris__membre__id=membre_id)
    
    
    contexte = {
        "paiements": paiements, 
        "evenement": evenement, 
        'membres': Membre.objects.all(), 
        "reinscris": reinscris,
        'selected_membre': int(membre_id) if membre_id else None,
        
        }
    return render(request, "gestionPaiement/paiementParEvenement.html", contexte)



@login_required
def detailPaimentMembre(request, pk):
    """
    Vue pour afficher les détails d'un paiement
    """
    paiement = get_object_or_404(Paiement, pk=pk)
    
    context = {
        'paiement': paiement,
    }
    
    return render(request, 'gestionPaiement/detailPaimentMembre.html', context)


@login_required
def supprimer_paiement(request, pk_membre, pk_evenement):
    """
    Vue pour supprimer un paiement
    """
    paiement = get_object_or_404(Paiement, pk=pk_membre)
    evenement = get_object_or_404(Evenement, pk=pk_evenement)
    
    try:
        membre_nom = paiement.membre_Reinscris.membre.nom_complet
        paiement.delete()
        messages.success(request, f'Paiement de {membre_nom} supprimé avec succès!')
        return redirect('paiementParEvenement', pk=pk_evenement)
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression: {str(e)}')
        return redirect('paiementParEvenement', pk=pk_evenement)


@login_required
@admin_required
def reinscriptionUser(request):
    if request.method == 'POST':
        form = ReinscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if not user:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
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





