from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from secondApp.models import EquipeDirigeante, Evenement, EvenementImage, Temoingnage, TypeEvenement, Membre, Utilisateur
from secondApp.forms import MembreInscriptionForm
from django.contrib import messages

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


def connexion(request):
    """
    Vue de connexion avec redirection selon le rôle
    """
    # Si déjà connecté, rediriger selon le rôle
    if request.user.is_authenticated:
        return rediriger_selon_role(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        
        # Debug - Afficher dans la console (à retirer en production)
        print(f"=== TENTATIVE DE CONNEXION ===")
        print(f"Username/Email: {username}")
        print(f"Password length: {len(password)}")
        
        # Validation basique
        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'user/connexion.html', {'next': request.GET.get('next', '')})
        
        user = None
        
        # 1. Essayer d'authentifier avec le username
        user = authenticate(request, username=username, password=password)
        print(f"Auth par username: {user}")
        
        # 2. Si échec, essayer avec l'email
        if user is None:
            try:
                # Chercher l'utilisateur par email
                user_obj = Utilisateur.objects.get(email__iexact=username)
                print(f"Utilisateur trouvé par email: {user_obj.username}")
                
                # Authentifier avec le username trouvé
                user = authenticate(request, username=user_obj.username, password=password)
                print(f"Auth par email: {user}")
                
            except Utilisateur.DoesNotExist:
                print(f"Aucun utilisateur avec l'email: {username}")
            except Utilisateur.MultipleObjectsReturned:
                print(f"Plusieurs utilisateurs avec l'email: {username}")
                messages.error(request, "Erreur: plusieurs comptes avec cet email. Contactez l'administrateur.")
                return render(request, 'user/connexion.html', {'next': request.GET.get('next', '')})
        
        # 3. Vérifier si l'authentification a réussi
        if user is not None:
            print(f"Utilisateur authentifié: {user.username}")
            print(f"Est actif: {user.is_active}")
            print(f"Est superuser: {user.is_superuser}")
            print(f"Rôle: {user.role}")
            
            # Vérifier si le compte est actif
            if not user.is_active:
                messages.error(request, "Votre compte a été désactivé. Contactez l'administrateur.")
                return render(request, 'user/connexion.html', {'next': request.GET.get('next', '')})
            
            # Connexion
            login(request, user)
            print(f"Connexion réussie pour: {user.username}")
            
            # Gérer "Se souvenir de moi"
            if remember_me:
                request.session.set_expiry(1209600)  # 2 semaines
            else:
                request.session.set_expiry(0)  # Expire à la fermeture du navigateur
            
            # Message de bienvenue
            prenom = user.first_name or user.username
            messages.success(request, f"Bienvenue {prenom} !")
            
            # Redirection
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url != '':
                print(f"Redirection vers next: {next_url}")
                return redirect(next_url)
            
            print(f"Redirection selon rôle...")
            return rediriger_selon_role(user)
        else:
            # Échec de l'authentification
            print(f"Échec de l'authentification pour: {username}")
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
    
    # GET request
    context = {
        'next': request.GET.get('next', '')
    }
    return render(request, 'user/connexion.html', context)


def rediriger_selon_role(user):
    """
    Redirige l'utilisateur selon son rôle
    """
    print(f"=== REDIRECTION SELON RÔLE ===")
    print(f"User: {user.username}")
    print(f"is_superuser: {user.is_superuser}")
    print(f"est_membre_equipe(): {user.est_membre_equipe()}")
    
    # Superuser ou membre de l'équipe → Dashboard
    if user.is_superuser or user.est_membre_equipe():
        print("-> Redirection vers admin_dashboard")
        return redirect('admin_dashboard')
    
    # Membre lambda → Page d'accueil
    print("-> Redirection vers index")
    return redirect('index')


@login_required(login_url='connexion')
def deconnexion(request):
    """
    Déconnexion de l'utilisateur
    """
    prenom = request.user.first_name or request.user.username
    logout(request)
    messages.info(request, f"Au revoir {prenom} ! Vous avez été déconnecté.")
    return redirect('index')


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

def affichageEvenement(request, id):  
    evenement = TypeEvenement.objects.get(id = id)
    evenementsFiltrer = Evenement.objects.filter(typeEvenement__id = id)
    return render(request, 'dynamiquePart/affichageEvenement.html', {'evenement': evenement, 'evenementsFiltrer': evenementsFiltrer})

def detailEvenement(request, id):
    evenement = Evenement.objects.get(id=id)
    evenementImage = EvenementImage.objects.filter(evenement=evenement)
    return render(request, 'user/detailEvenement.html', {'evenement': evenement, 'evenementImage': evenementImage})


