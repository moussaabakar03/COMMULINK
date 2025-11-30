
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Annee, Membre, Annonce, Paiement, EquipeDirigeante, Evenement, EvenementImage, Reinscription, Temoingnage, TypeEvenement, Utilisateur
from .forms import AnneeForm, MembreForm, AnnonceForm, PaiementForm, ReinscriptionForm, MembreInscriptionForm, MembreModificationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mass_mail
from django.views.decorators.http import require_POST
# from time import timezone
from django.db import transaction
import datetime
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


# DASHBOARD VIEW
@login_required
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

# ============================================
# INSCRIPTION PUBLIQUE (Demande en attente)
# ============================================


def inscription_confirmation(request, pk):
    """Page de confirmation après inscription"""
    membre = get_object_or_404(Membre, pk=pk)
    return render(request, 'gestionMembre/inscription_confirmation.html', {
        'membre': membre
    })


# ============================================
# CRÉATION DIRECTE (Admin - Validé directement)
# ============================================

@login_required
def creer_membre(request):
    """
    Création directe par un admin - Crée membre + utilisateur + réinscription
    Le membre est directement validé
    """
    # Vérifier les droits
    if not request.user.est_membre_equipe():
        messages.error(request, "Vous n'avez pas les droits pour créer un membre.")
        return redirect('liste_membres')
    
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    nom = form.cleaned_data['nom']
                    prenom = form.cleaned_data['prenom']
                    email = form.cleaned_data['email']
                    telephone = form.cleaned_data.get('telephone') or "defaultpass123"
                    
                    # Vérification supplémentaire
                    if Utilisateur.objects.filter(email=email).exists():
                        messages.error(request, 'Un utilisateur avec cet email existe déjà.')
                        return render(request, 'gestionMembre/creer.html', {'form': form})
                    
                    # 1. Créer l'utilisateur
                    utilisateur = Utilisateur.objects.create(
                        username=email,
                        email=email,
                        password=make_password(telephone),
                        first_name=prenom,
                        last_name=nom,
                        role="membreLambda",
                        is_active=True,
                    )
                    
                    # 2. Créer le membre (validé directement)
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
                        statut='valide',  # Validé directement
                        date_validation=timezone.now(),
                        valide_par=request.user,
                    )
                    
                    if form.cleaned_data.get('photo'):
                        membre.photo = form.cleaned_data['photo']
                    
                    membre.save()
                    
                    # 3. Créer la réinscription pour l'année active
                    annee_active = Annee.objects.order_by('-debutAnnee').first()
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
                    return redirect('detail_membre', pk=membre.pk)
                    
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreForm()
    
    return render(request, 'gestionMembre/creer.html', {
        'form': form,
        'titre': "Créer un nouveau membre"
    })


# ============================================
# VALIDATION DES DEMANDES
# ============================================

from io import BytesIO
try:
    from xhtml2pdf import pisa
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False
    print("xhtml2pdf non installé. L'export PDF sera désactivé.")


def get_annee_active():
    """Récupère l'année active ou la plus récente"""
    today = timezone.now().date()
    annee = Annee.objects.filter(
        debutAnnee__lte=today,
        finAnnee__gte=today
    ).first()
    
    if not annee:
        annee = Annee.objects.order_by('-debutAnnee').first()
    
    return annee

@login_required
def valider_membre(request, pk):
    """
    Valide une demande d'inscription
    Crée l'utilisateur et la réinscription lors de la validation
    """
    membre = get_object_or_404(Membre, pk=pk)
    
    if not request.user.est_membre_equipe():
        messages.error(request, "Vous n'avez pas les droits pour valider les inscriptions.")
        return redirect('liste_membres')
    
    if membre.statut != 'en_attente':
        messages.warning(request, f"Ce membre a déjà été traité (statut: {membre.get_statut_display()}).")
        return redirect('liste_membres')
    
    try:
        with transaction.atomic():
            email = membre.email
            telephone = membre.telephone or "defaultpass123"
            
            # Vérifier si un utilisateur existe déjà avec cet email
            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, f"Un utilisateur avec l'email {email} existe déjà.")
                return redirect('liste_membres')
            
            # 1. Créer l'utilisateur avec create_user pour hasher le mot de passe
            utilisateur = Utilisateur.objects.create_user(
                username=email,
                email=email,
                password=telephone,
                first_name=membre.prenom,
                last_name=membre.nom,
            )
            utilisateur.role = "membreLambda"
            utilisateur.is_active = True
            utilisateur.save()
            
            # 2. Mettre à jour le membre
            membre.utilisateur = utilisateur
            membre.statut = 'valide'
            membre.date_validation = timezone.now()
            membre.valide_par = request.user
            membre.save()
            
            # 3. Créer la réinscription pour l'année active
            annee_active = get_annee_active()
            if annee_active:
                # Extraire la filière des notes si présente
                filiere = ''
                if membre.notes and 'Filière:' in membre.notes:
                    for line in membre.notes.split('\n'):
                        if line.startswith('Filière:'):
                            filiere = line.replace('Filière:', '').strip()
                            break
                
                Reinscription.objects.create(
                    membre=membre,
                    annee=annee_active,
                    username=email,
                    password=telephone,
                    adresse=membre.adresse or '',
                    numeroUrgence=membre.numeroUrgence or '',
                    ecole=membre.ecole or '',
                    niveauEtude=membre.niveauEtude or '',
                    photo_annuelle=membre.photo if membre.photo else None,
                    filiere=filiere
                )
            
            messages.success(request, f"L'inscription de {membre.nom_complet} a été validée avec succès. Mot de passe: {telephone}")
            
    except Exception as e:
        import traceback
        print(f"Erreur validation: {e}")
        print(traceback.format_exc())
        messages.error(request, f"Erreur lors de la validation: {str(e)}")
    
    return redirect('liste_membres')


@login_required
def refuser_membre(request, pk):
    """Refuse une demande d'inscription"""
    membre = get_object_or_404(Membre, pk=pk)
    
    if not request.user.est_membre_equipe():
        messages.error(request, "Vous n'avez pas les droits pour refuser les inscriptions.")
        return redirect('liste_membres')
    
    if membre.statut != 'en_attente':
        messages.warning(request, f"Ce membre a déjà été traité (statut: {membre.get_statut_display()}).")
        return redirect('liste_membres')
    
    try:
        membre.statut = 'refuse'
        membre.date_validation = timezone.now()
        membre.valide_par = request.user
        membre.save()
        
        messages.info(request, f"L'inscription de {membre.nom_complet} a été refusée.")
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
    
    return redirect('liste_membres')


@login_required
@require_POST
def valider_membre_ajax(request, pk):
    """Valide une demande d'inscription via AJAX"""
    
    membre = get_object_or_404(Membre, pk=pk)
    
    if not request.user.est_membre_equipe():
        return JsonResponse({
            'success': False, 
            'message': "Vous n'avez pas les droits pour cette action."
        }, status=403)
    
    if membre.statut != 'en_attente':
        return JsonResponse({
            'success': False,
            'message': "Ce membre a déjà été traité."
        })
    
    try:
        with transaction.atomic():
            email = membre.email
            telephone = membre.telephone or "defaultpass123"
            
            # Vérifier si un utilisateur existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': f"Un utilisateur avec l'email {email} existe déjà."
                })
            
            if Utilisateur.objects.filter(username=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': f"Un utilisateur avec ce nom d'utilisateur existe déjà."
                })
            
            # 1. Créer l'utilisateur
            utilisateur = Utilisateur.objects.create_user(
                username=email,
                email=email,
                password=telephone,
                first_name=membre.prenom,
                last_name=membre.nom,
            )
            utilisateur.role = "membreLambda"
            utilisateur.is_active = True
            utilisateur.save()
            
            # 2. Mettre à jour le membre
            membre.utilisateur = utilisateur
            membre.statut = 'valide'
            membre.date_validation = timezone.now()
            membre.valide_par = request.user
            membre.save()
            
            # 3. Créer la réinscription
            annee_active = get_annee_active()
            if annee_active:
                filiere = ''
                if membre.notes and 'Filière:' in membre.notes:
                    for line in membre.notes.split('\n'):
                        if line.startswith('Filière:'):
                            filiere = line.replace('Filière:', '').strip()
                            break
                
                Reinscription.objects.create(
                    membre=membre,
                    annee=annee_active,
                    username=email,
                    password=telephone,
                    adresse=membre.adresse or '',
                    numeroUrgence=membre.numeroUrgence or '',
                    ecole=membre.ecole or '',
                    niveauEtude=membre.niveauEtude or '',
                    photo_annuelle=membre.photo if membre.photo else None,
                    filiere=filiere
                )
            
            return JsonResponse({
                'success': True,
                'message': f"L'inscription de {membre.nom_complet} a été validée.",
                'nouveau_statut': 'valide',
                'nouveau_statut_display': 'Validé'
            })
            
    except Exception as e:
        import traceback
        print(f"Erreur AJAX validation: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f"Erreur: {str(e)}"
        })


@login_required
@require_POST
def refuser_membre_ajax(request, pk):
    """Refuse une demande d'inscription via AJAX"""
    
    membre = get_object_or_404(Membre, pk=pk)
    
    if not request.user.est_membre_equipe():
        return JsonResponse({
            'success': False, 
            'message': "Vous n'avez pas les droits pour cette action."
        }, status=403)
    
    if membre.statut != 'en_attente':
        return JsonResponse({
            'success': False,
            'message': "Ce membre a déjà été traité."
        })
    
    try:
        membre.statut = 'refuse'
        membre.date_validation = timezone.now()
        membre.valide_par = request.user
        membre.save()
        
        return JsonResponse({
            'success': True,
            'message': f"L'inscription de {membre.nom_complet} a été refusée.",
            'nouveau_statut': 'refuse',
            'nouveau_statut_display': 'Refusé'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Erreur: {str(e)}"
        })


@login_required
@require_POST
def valider_tous_en_attente(request):
    """Valide toutes les demandes en attente"""
    
    if not request.user.est_membre_equipe():
        messages.error(request, "Vous n'avez pas les droits pour cette action.")
        return redirect('liste_membres')
    
    membres_en_attente = Membre.objects.filter(statut='en_attente')
    count_success = 0
    count_error = 0
    errors = []
    
    annee_active = get_annee_active()
    
    for membre in membres_en_attente:
        try:
            with transaction.atomic():
                email = membre.email
                telephone = membre.telephone or "defaultpass123"
                
                # Vérifier si l'utilisateur existe déjà
                if Utilisateur.objects.filter(email=email).exists():
                    count_error += 1
                    errors.append(f"{membre.nom_complet}: email déjà utilisé")
                    continue
                
                if Utilisateur.objects.filter(username=email).exists():
                    count_error += 1
                    errors.append(f"{membre.nom_complet}: username déjà utilisé")
                    continue
                
                # Créer l'utilisateur
                utilisateur = Utilisateur.objects.create_user(
                    username=email,
                    email=email,
                    password=telephone,
                    first_name=membre.prenom,
                    last_name=membre.nom,
                )
                utilisateur.role = "membreLambda"
                utilisateur.is_active = True
                utilisateur.save()
                
                # Mettre à jour le membre
                membre.utilisateur = utilisateur
                membre.statut = 'valide'
                membre.date_validation = timezone.now()
                membre.valide_par = request.user
                membre.save()
                
                # Créer la réinscription
                if annee_active:
                    filiere = ''
                    if membre.notes and 'Filière:' in membre.notes:
                        for line in membre.notes.split('\n'):
                            if line.startswith('Filière:'):
                                filiere = line.replace('Filière:', '').strip()
                                break
                    
                    Reinscription.objects.create(
                        membre=membre,
                        annee=annee_active,
                        username=email,
                        password=telephone,
                        adresse=membre.adresse or '',
                        numeroUrgence=membre.numeroUrgence or '',
                        ecole=membre.ecole or '',
                        niveauEtude=membre.niveauEtude or '',
                        photo_annuelle=membre.photo if membre.photo else None,
                        filiere=filiere
                    )
                
                count_success += 1
                
        except Exception as e:
            count_error += 1
            errors.append(f"{membre.nom_complet}: {str(e)}")
            print(f"Erreur validation en masse {membre.email}: {e}")
    
    if count_success > 0:
        messages.success(request, f"{count_success} inscription(s) validée(s) avec succès.")
    
    if count_error > 0:
        error_msg = f"{count_error} inscription(s) n'ont pas pu être validées."
        if errors:
            error_msg += " Détails: " + "; ".join(errors[:3])  # Afficher max 3 erreurs
            if len(errors) > 3:
                error_msg += f" et {len(errors) - 3} autre(s)..."
        messages.warning(request, error_msg)
    
    return redirect('liste_membres') 


# ============================================
# LISTE ET DÉTAILS
# ============================================

def liste_membres(request):
    """Liste des membres avec filtres par statut et par année"""
    
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', 'tous')
    annee_filter = request.GET.get('annee', '')
    
    # Récupérer toutes les années pour le filtre
    annees = Annee.objects.all().order_by('-debutAnnee')
    
    # Base queryset
    membres = Membre.objects.all()
    
    # Filtrer par année (via les réinscriptions)
    if annee_filter:
        try:
            annee_id = int(annee_filter)
            membres = membres.filter(reinscriptions__annee_id=annee_id).distinct()
        except (ValueError, TypeError):
            pass
    
    # Filtrer par statut
    if statut_filter == 'en_attente':
        membres = membres.filter(statut='en_attente')
    elif statut_filter == 'valide':
        membres = membres.filter(statut='valide')
    elif statut_filter == 'refuse':
        membres = membres.filter(statut='refuse')
    
    # Filtrer par recherche
    if search_query:
        membres = membres.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(ner__icontains=search_query) |
            Q(keri__icontains=search_query) |
            Q(ecole__icontains=search_query)
        )
    
    membres = membres.order_by('-date_inscription', 'nom', 'prenom')
    nombreMembre = membres.count()
    
    # Compteurs
    if annee_filter:
        try:
            annee_id = int(annee_filter)
            base_qs = Membre.objects.filter(reinscriptions__annee_id=annee_id).distinct()
        except:
            base_qs = Membre.objects.all()
    else:
        base_qs = Membre.objects.all()
    
    nombre_en_attente = base_qs.filter(statut='en_attente').count()
    nombre_valide = base_qs.filter(statut='valide').count()
    nombre_refuse = base_qs.filter(statut='refuse').count()
    
    # Pagination
    paginator = Paginator(membres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Année sélectionnée pour l'affichage
    annee_selectionnee = None
    if annee_filter:
        try:
            annee_selectionnee = Annee.objects.get(pk=int(annee_filter))
        except:
            pass
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'annee_filter': annee_filter,
        'annees': annees,
        'annee_selectionnee': annee_selectionnee,
        'nombreMembre': nombreMembre,
        'nombre_en_attente': nombre_en_attente,
        'nombre_valide': nombre_valide,
        'nombre_refuse': nombre_refuse,
        'pdf_enabled': PDF_ENABLED,
    }
    
    return render(request, 'gestionMembre/liste.html', context)


@login_required
def exporter_membres_pdf(request):
    """Exporte la liste des membres en PDF"""
    
    if not PDF_ENABLED:
        messages.error(request, "L'export PDF n'est pas disponible. Installez xhtml2pdf.")
        return redirect('liste_membres')
    
    # Récupérer les mêmes filtres que la liste
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', 'tous')
    annee_filter = request.GET.get('annee', '')
    
    # Base queryset
    membres = Membre.objects.all()
    
    # Filtrer par année
    if annee_filter:
        try:
            annee_id = int(annee_filter)
            membres = membres.filter(reinscriptions__annee_id=annee_id).distinct()
        except (ValueError, TypeError):
            pass
    
    # Filtrer par statut
    if statut_filter == 'en_attente':
        membres = membres.filter(statut='en_attente')
    elif statut_filter == 'valide':
        membres = membres.filter(statut='valide')
    elif statut_filter == 'refuse':
        membres = membres.filter(statut='refuse')
    
    # Filtrer par recherche
    if search_query:
        membres = membres.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(ner__icontains=search_query) |
            Q(keri__icontains=search_query)
        )
    
    membres = membres.order_by('nom', 'prenom')
    
    # Année sélectionnée
    annee_selectionnee = None
    if annee_filter:
        try:
            annee_selectionnee = Annee.objects.get(pk=int(annee_filter))
        except:
            pass
    
    # Générer le PDF
    context = {
        'membres': membres,
        'total': membres.count(),
        'statut_filter': statut_filter,
        'annee_selectionnee': annee_selectionnee,
        'search_query': search_query,
        'date_export': timezone.now(),
        'exporteur': request.user if request.user.is_authenticated else None,
    }
    
    template = get_template('gestionMembre/export_pdf.html')
    html = template.render(context)
    
    # Créer le PDF
    response = HttpResponse(content_type='application/pdf')
    
    # Nom du fichier
    filename = f"liste_membres_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Générer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        messages.error(request, "Erreur lors de la génération du PDF.")
        return redirect('liste_membres')
    
    return response


@login_required
def exporter_membres_csv(request):
    """Exporte la liste des membres en CSV"""
    import csv
    
    # Récupérer les mêmes filtres
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', 'tous')
    annee_filter = request.GET.get('annee', '')
    
    # Base queryset
    membres = Membre.objects.all()
    
    # Filtrer par année
    if annee_filter:
        try:
            annee_id = int(annee_filter)
            membres = membres.filter(reinscriptions__annee_id=annee_id).distinct()
        except:
            pass
    
    # Filtrer par statut
    if statut_filter == 'en_attente':
        membres = membres.filter(statut='en_attente')
    elif statut_filter == 'valide':
        membres = membres.filter(statut='valide')
    elif statut_filter == 'refuse':
        membres = membres.filter(statut='refuse')
    
    # Filtrer par recherche
    if search_query:
        membres = membres.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    membres = membres.order_by('nom', 'prenom')
    
    # Créer la réponse CSV
    response = HttpResponse(content_type='text/csv')
    filename = f"liste_membres_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('\ufeff'.encode('utf8'))  # BOM pour Excel
    
    writer = csv.writer(response, delimiter=';')
    
    # En-têtes
    writer.writerow([
        'Nom', 'Prénom', 'Email', 'Téléphone', 'Sexe',
        'Profession', 'École', 'Niveau d\'étude',
        'Ner', 'Keri', 'Keribour',
        'Adresse', 'Statut', 'Date inscription'
    ])
    
    # Données
    for membre in membres:
        writer.writerow([
            membre.nom,
            membre.prenom,
            membre.email,
            membre.telephone or '',
            membre.get_sexe_display() if hasattr(membre, 'get_sexe_display') else membre.sexe,
            membre.profession,
            membre.ecole or '',
            membre.niveauEtude or '',
            membre.ner or '',
            membre.keri or '',
            membre.keribour or '',
            membre.adresse or '',
            membre.get_statut_display() if hasattr(membre, 'get_statut_display') else membre.statut,
            membre.date_inscription.strftime('%d/%m/%Y') if membre.date_inscription else '',
        ])
    
    return response


def detail_membre(request, pk):
    """Détails d'un membre"""
    membre = get_object_or_404(Membre, pk=pk)
    
    peut_modifier = False
    if request.user.is_authenticated:
        if request.user.est_membre_equipe():
            peut_modifier = True
        elif hasattr(request.user, 'membre') and request.user.membre.pk == pk:
            peut_modifier = True
    
    # Récupérer les réinscriptions
    reinscriptions = []
    if hasattr(membre, 'reinscriptions'):
        reinscriptions = membre.reinscriptions.all().order_by('-annee__id')
    
    return render(request, 'gestionMembre/detail.html', {
        'membre': membre,
        'peut_modifier': peut_modifier,
        'reinscriptions': reinscriptions,
    })


# ============================================
# MODIFICATION ET SUPPRESSION
# ============================================

@login_required
def modifier_membre(request, pk):
    """Modifier un membre existant"""
    membre = get_object_or_404(Membre, pk=pk)
    
    # Vérifier les droits
    if not request.user.est_membre_equipe():
        if not hasattr(request.user, 'membre') or request.user.membre.pk != pk:
            messages.error(request, "Vous n'avez pas les droits pour modifier ce profil.")
            return redirect('liste_membres')
    
    if request.method == 'POST':
        form = MembreModificationForm(request.POST, request.FILES, instance=membre)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Mettre à jour le membre
                    membre.nom = form.cleaned_data['nom']
                    membre.prenom = form.cleaned_data['prenom']
                    membre.sexe = form.cleaned_data['sexe']
                    membre.email = form.cleaned_data['email']
                    membre.telephone = form.cleaned_data.get('telephone', '')
                    membre.adresse = form.cleaned_data.get('adresse', '')
                    membre.profession = form.cleaned_data['profession']
                    membre.numeroUrgence = form.cleaned_data.get('numeroUrgence', '')
                    membre.niveauEtude = form.cleaned_data.get('niveauEtude', '')
                    membre.ecole = form.cleaned_data.get('ecole', '')
                    membre.ner = form.cleaned_data.get('ner', '')
                    membre.keri = form.cleaned_data.get('keri', '')
                    membre.keribour = form.cleaned_data.get('keribour', '')
                    membre.keriBa = form.cleaned_data.get('keriBa', '')
                    membre.keribourBa = form.cleaned_data.get('keribourBa', '')
                    membre.notes = form.cleaned_data.get('notes', '')
                    
                    if form.cleaned_data.get('photo'):
                        membre.photo = form.cleaned_data['photo']
                    
                    membre.save()
                    
                    # Mettre à jour l'utilisateur associé si existe
                    if membre.utilisateur:
                        membre.utilisateur.email = form.cleaned_data['email']
                        membre.utilisateur.username = form.cleaned_data['email']
                        membre.utilisateur.first_name = form.cleaned_data['prenom']
                        membre.utilisateur.last_name = form.cleaned_data['nom']
                        membre.utilisateur.save()
                    
                    messages.success(request, f"Le profil de {membre.nom_complet} a été mis à jour.")
                    return redirect('detail_membre', pk=membre.pk)
                    
            except Exception as e:
                messages.error(request, f"Erreur lors de la modification: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MembreModificationForm(instance=membre)
    
    return render(request, 'gestionMembre/modifierMembre.html', {
        'form': form,
        'membre': membre,
        'titre': f"Modifier le profil de {membre.nom_complet}"
    })


@login_required
def supprimer_membre(request, pk):
    """Supprimer un membre"""
    membre = get_object_or_404(Membre, pk=pk)
    
    if not request.user.est_membre_equipe():
        messages.error(request, "Vous n'avez pas les droits pour supprimer un membre.")
        return redirect('liste_membres')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                nom_complet = membre.nom_complet
                
                # Supprimer l'utilisateur associé si existe
                if membre.utilisateur:
                    membre.utilisateur.delete()
                
                membre.delete()
                messages.success(request, f"Le membre {nom_complet} a été supprimé avec succès.")
                
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression: {str(e)}")
        
        return redirect('liste_membres')
    
    # return render(request, 'gestionMembre/supprimer_membre.html', {
    #     'membre': membre
    # })


# ============================================
# API
# ============================================

def verifier_email_disponible(request):
    """API pour vérifier si un email est disponible"""
    email = request.GET.get('email', '')
    membre_pk = request.GET.get('membre_pk')  # Pour exclure lors de la modification
    
    if not email:
        return JsonResponse({'disponible': False, 'message': 'Email requis'})
    
    # Vérifier dans les membres
    membre_qs = Membre.objects.filter(email=email)
    if membre_pk:
        membre_qs = membre_qs.exclude(pk=membre_pk)
    
    # Vérifier dans les utilisateurs
    user_qs = Utilisateur.objects.filter(email=email)
    
    existe = membre_qs.exists() or user_qs.exists()
    
    return JsonResponse({
        'disponible': not existe,
        'message': 'Cet email est déjà utilisé' if existe else 'Email disponible'
    })


#======================================GESTION EQUIPE DIRRIGEANTE===============================
def liste_equipe_dirigeante(request):
    """Liste des membres de l'équipe dirigeante"""
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', 'tous')
    role_filter = request.GET.get('role', '')
    
    # Base queryset
    membres = EquipeDirigeante.objects.all()
    
    # Filtrer par statut
    if statut_filter == 'actif':
        membres = membres.filter(actif=True)
    elif statut_filter == 'inactif':
        membres = membres.filter(actif=False)
    
    # Filtrer par rôle
    if role_filter:
        membres = membres.filter(role=role_filter)
    
    # Recherche
    if search_query:
        membres = membres.filter(
            Q(nom__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    membres = membres.order_by('ordre', 'nom')
    total_membres = membres.count()
    
    # Compteurs
    nombre_actifs = EquipeDirigeante.objects.filter(actif=True).count()
    nombre_inactifs = EquipeDirigeante.objects.filter(actif=False).count()
    
    # Liste des rôles pour le filtre
    roles_disponibles = EquipeDirigeante.ROLE_CHOICES
    
    # Pagination
    paginator = Paginator(membres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'role_filter': role_filter,
        'total_membres': total_membres,
        'nombre_actifs': nombre_actifs,
        'nombre_inactifs': nombre_inactifs,
        'roles_disponibles': roles_disponibles,
    }
    
    return render(request, 'gestionMembre/listeMembreEquipe.html', context)


#-----------------------------GESTION ANNONCES--------------------------------------------------


def liste_annonces(request):
    search_query = request.GET.get("search", "")

    if search_query:
        annonces = Annonce.objects.filter(titre__icontains=search_query).order_by('-date_creation')
    else:
        annonces = Annonce.objects.all().order_by('-date_creation')

    return render(request, 'gestionAnnonce/liste.html', {'annonces': annonces})


@login_required
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
def publier_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    annonce.est_publie = True
    annonce.date_publication = datetime.datetime.now()
    annonce.save()
    messages.success(request, "Annonce publiée avec succès")
    return redirect('liste_annonces')


@login_required
def depublier_annonce(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    annonce.est_publie = False
    annonce.save()
    messages.success(request, "Annonce dépubliée avec succès")
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
                    'admin@example.com', 
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
    
    # 2. Récupérer les IDs des membres déjà réinscrits et ayant fait un paiement
    membres_ayant_paye = paiements.values_list('membre_Reinscris_id', flat=True)

    # 3. Trouver les réinscriptions de l'année en excluant ceux qui ont payé
    reinscris = Reinscription.objects.filter(annee=evenement.annee).exclude(id__in=membres_ayant_paye)

    
    membre_id = request.GET.get('membre')
    if membre_id:
        paiements = paiements.filter(membre__id=membre_id)
    
    
    contexte = {"paiements": paiements, "evenement": evenement, 'membres': Membre.objects.all(), "reinscris": reinscris}
    return render(request, "gestionPaiement/paiementParEvenement.html", contexte)



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





