from django import forms
from django.contrib.auth import authenticate

from django.core.validators import MinLengthValidator, EmailValidator, RegexValidator
from django.utils import timezone
from secondApp.forms import MembreForm
from secondApp.models import Annee, Membre, Utilisateur

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ConnexionForm(forms.Form):
    identifiant = forms.CharField(
        label='Email ou Username * :',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'id': 'login-password', 'placeholder': 'Votre mot de passe', 'required': 'required'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifiant = cleaned_data.get('identifiant')
        password = cleaned_data.get('password')

        if identifiant and password:
            user = authenticate(request=self.request, username=identifiant, password=password)
            if user is None:
                raise forms.ValidationError("Identifiant ou mot de passe incorrect.")
            if not user.is_active:
                raise forms.ValidationError("Ce compte est désactivé.")
            cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')



class MembreInscriptionForm(forms.ModelForm):
    """
    Formulaire d'inscription publique pour les membres
    """
    
    class Meta:
        model = Membre
        fields = [
            'nom', 'prenom', 'sexe', 'email', 'telephone',
            'niveauEtude', 'ecole', 'filiere',
            'numeroUrgence', 'ner', 'keri', 'keribour', 
            'keriBa', 'keribourBa', 'adresse', 'photo', 'notes',
            'nom_utilisateur', 'mot_de_passe',
        ]
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom de famille',
                'maxlength': 150,
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre prénom',
                'maxlength': 150,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre.email@exemple.com',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre numéro de téléphone',
                'maxlength': 20,
            }),
            'sexe': forms.RadioSelect(attrs={
                'class': 'radio-input'
            }),
            'niveauEtude': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre niveau d\'étude',
                'maxlength': 20,
            }),
            'ecole': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom de votre établissement',
                'maxlength': 20,
            }),
            'filiere': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre filière d\'étude',
                'maxlength': 20,
            }),
            'numeroUrgence': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Numéro d\'une personne à contacter',
                'maxlength': 20,
            }),
            'ner': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez la valeur pour Ner',
                'maxlength': 20,
            }),
            'keri': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez la valeur pour Keri',
                'maxlength': 20,
            }),
            'keribour': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez la valeur pour Keribour',
                'maxlength': 20,
            }),
            'keriBa': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez la valeur pour Keri Bâ',
                'maxlength': 20,
            }),
            'keribourBa': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez la valeur pour Keribour Bâ',
                'maxlength': 20,
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Votre adresse complète (rue, ville, code postal)',
                'rows': 4,
            }),
            'photo': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Ajoutez ici toute information complémentaire...',
                'rows': 4,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Champs obligatoires
        self.fields['nom'].required = True
        self.fields['prenom'].required = True
        self.fields['email'].required = True
        self.fields['sexe'].required = True
        self.fields['nom_utilisateur'].required = True
        self.fields['mot_de_passe'].required = True
        
        # Champs optionnels
        optional_fields = [
            'telephone', 'niveauEtude', 'ecole', 'filiere',
            'numeroUrgence', 'ner', 'keri', 'keribour',
            'keriBa', 'keribourBa', 'adresse', 'photo', 'notes'
        ]
        for field in optional_fields:
            self.fields[field].required = False
    
    def clean_email(self):
        """Valider l'unicité de l'email"""
        email = self.cleaned_data.get('email')
        if email:
            # Vérifier si l'email existe déjà (exclure l'instance actuelle si modification)
            qs = Membre.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email
    
    def clean(self):
        """Validation globale du formulaire"""
        cleaned_data = super().clean()
        
        # Vérifier qu'au moins un champ d'identité est rempli
        identite_fields = ['ner', 'keri', 'keribour', 'keriBa', 'keribourBa']
        has_identite = any(cleaned_data.get(field) for field in identite_fields)
        
        if not has_identite:
            raise forms.ValidationError(
                "Veuillez remplir au moins un des champs d'identité "
                "(Ner, Keri, Keribour, Keri Bâ, ou Keribour Bâ)."
            )
        
        return cleaned_data

class MembreModificationForm(MembreForm):
    """Formulaire pour modifier un membre existant"""
    
    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'nom': instance.nom,
                'prenom': instance.prenom,
                'sexe': instance.sexe,
                'email': instance.email,
                'telephone': instance.telephone or '',
                'adresse': instance.adresse or '',
                'numeroUrgence': instance.numeroUrgence or '',
                'niveauEtude': instance.niveauEtude or '',
                'ecole': instance.ecole or '',
                'ner': instance.ner or '',
                'keri': instance.keri or '',
                'keribour': instance.keribour or '',
                'keriBa': instance.keriBa or '',
                'keribourBa': instance.keribourBa or '',
                'notes': instance.notes or '',
            })
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Vérifie que l'email n'est pas déjà utilisé par un autre membre"""
        email = self.cleaned_data.get('email')
        
        # Exclure le membre actuel de la vérification
        membre_qs = Membre.objects.filter(email=email)
        if self.instance:
            membre_qs = membre_qs.exclude(pk=self.instance.pk)
        
        if membre_qs.exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre membre.")
        
        # Vérifier aussi les utilisateurs (en excluant l'utilisateur lié au membre)
        user_qs = Utilisateur.objects.filter(email=email)
        if self.instance and self.instance.utilisateur:
            user_qs = user_qs.exclude(pk=self.instance.utilisateur.pk)
        
        if user_qs.exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        
        return email

    """Formulaire d'inscription pour les nouveaux membres"""
    
    GENRE_CHOICES = [
        ('', 'Sélectionnez votre genre'),
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    
    NIVEAU_ETUDE_CHOICES = [
        ('', 'Sélectionnez votre niveau'),
        ('primaire', 'Primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('bac', 'Baccalauréat'),
        ('bac+2', 'Bac +2'),
        ('bac+3', 'Bac +3 (Licence)'),
        ('bac+5', 'Bac +5 (Master)'),
        ('bac+8', 'Bac +8 (Doctorat)'),
        ('autre', 'Autre'),
    ]

    # Informations personnelles
    nom = forms.CharField(
        max_length=150,
        validators=[MinLengthValidator(2, "Le nom doit contenir au moins 2 caractères")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom de famille',
            'id': 'nom'
        }),
        label="Nom *"
    )
    
    prenom = forms.CharField(
        max_length=150,
        validators=[MinLengthValidator(2, "Le prénom doit contenir au moins 2 caractères")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
            'id': 'prenom'
        }),
        label="Prénom *"
    )
    
    sexe = forms.ChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'sexe'
        }),
        label="Genre *"
    )
    
    email = forms.EmailField(
        validators=[EmailValidator("Veuillez entrer une adresse email valide")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com',
            'id': 'email'
        }),
        label="Adresse email *"
    )
    
    telephone = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[\d\s\+\-\.]+$',
                message="Numéro de téléphone invalide"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+33 6 12 34 56 78',
            'id': 'telephone'
        }),
        label="Téléphone"
    )
    
    # Adresse
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Votre adresse complète',
            'id': 'adresse'
        }),
        label="Adresse"
    )
    
    # Informations professionnelles/scolaires
    
    niveauEtude = forms.ChoiceField(
        choices=NIVEAU_ETUDE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'niveauEtude'
        }),
        label="Niveau d'étude"
    )
    
    ecole = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom de votre école/université',
            'id': 'ecole'
        }),
        label="École/Université"
    )
    
    # Contact d'urgence
    numeroUrgence = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[\d\s\+\-\.]+$',
                message="Numéro de téléphone invalide"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro en cas d\'urgence',
            'id': 'numeroUrgence'
        }),
        label="Numéro d'urgence"
    )
    
    # Informations sur l'identité culturelle
    ner = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre ner',
            'id': 'ner'
        }),
        label="Ner"
    )
    
    keri = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre keri',
            'id': 'keri'
        }),
        label="Keri"
    )
    
    keribour = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre keribour',
            'id': 'keribour'
        }),
        label="Keribour"
    )
    
    keriBa = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Keri de votre père',
            'id': 'keriBa'
        }),
        label="Keri Ba (père)"
    )
    
    keribourBa = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Keribour de votre père',
            'id': 'keribourBa'
        }),
        label="Keribour Ba (père)"
    )
    
    # Photo et notes
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'photo',
            'accept': 'image/*'
        }),
        label="Photo de profil"
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Informations supplémentaires ou remarques...',
            'id': 'notes'
        }),
        label="Notes / Remarques"
    )
    
    # Acceptation des conditions
    accepte_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'accepte_conditions'
        }),
        label="J'accepte les conditions d'utilisation et la politique de confidentialité *"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Membre.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre membre.")
        return email

    def clean_sexe(self):
        """Vérifie qu'un genre a été sélectionné"""
        sexe = self.cleaned_data.get('sexe')
        if not sexe:
            raise forms.ValidationError("Veuillez sélectionner votre genre.")
        return sexe

    def clean_photo(self):
        """Valide la photo uploadée"""
        photo = self.cleaned_data.get('photo')
        if photo:
            # Vérifier la taille (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("La photo ne doit pas dépasser 5 Mo.")
            
            # Vérifier le type de fichier
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if photo.content_type not in allowed_types:
                raise forms.ValidationError("Format d'image non supporté. Utilisez JPG, PNG, GIF ou WebP.")
        return photo

    def save(self, commit=True):
        """Crée une nouvelle instance de Membre avec le statut 'en_attente'"""
        membre = Membre(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            sexe=self.cleaned_data['sexe'],
            email=self.cleaned_data['email'],
            telephone=self.cleaned_data.get('telephone', ''),
            adresse=self.cleaned_data.get('adresse', ''),
            numeroUrgence=self.cleaned_data.get('numeroUrgence', ''),
            niveauEtude=self.cleaned_data.get('niveauEtude', ''),
            ecole=self.cleaned_data.get('ecole', ''),
            ner=self.cleaned_data.get('ner', ''),
            keri=self.cleaned_data.get('keri', ''),
            keribour=self.cleaned_data.get('keribour', ''),
            keriBa=self.cleaned_data.get('keriBa', ''),
            keribourBa=self.cleaned_data.get('keribourBa', ''),
            notes=self.cleaned_data.get('notes', ''),
            statut='en_attente',  # Statut par défaut: en attente de validation
        )
        
        # Gestion de la photo
        if self.cleaned_data.get('photo'):
            membre.photo = self.cleaned_data['photo']
        
        if commit:
            membre.save()
        return membre


class MembreModificationForm(MembreInscriptionForm):
    """Formulaire de modification pour les membres existants"""
    
    # Pas besoin d'accepter les conditions pour une modification
    accepte_conditions = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        
        # Pré-remplir le formulaire avec les données existantes
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'nom': instance.nom,
                'prenom': instance.prenom,
                'sexe': instance.sexe,
                'email': instance.email,
                'telephone': instance.telephone or '',
                'adresse': instance.adresse or '',
                'numeroUrgence': instance.numeroUrgence or '',
                'niveauEtude': instance.niveauEtude or '',
                'ecole': instance.ecole or '',
                'ner': instance.ner or '',
                'keri': instance.keri or '',
                'keribour': instance.keribour or '',
                'keriBa': instance.keriBa or '',
                'keribourBa': instance.keribourBa or '',
                'notes': instance.notes or '',
            })
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Vérifie que l'email n'est pas déjà utilisé par un autre membre"""
        email = self.cleaned_data.get('email')
        queryset = Membre.objects.filter(email=email)
        
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre membre.")
        return email

    def save(self, commit=True):
        """Met à jour l'instance existante de Membre"""
        if not self.instance:
            return super().save(commit)
        
        self.instance.nom = self.cleaned_data['nom']
        self.instance.prenom = self.cleaned_data['prenom']
        self.instance.sexe = self.cleaned_data['sexe']
        self.instance.email = self.cleaned_data['email']
        self.instance.telephone = self.cleaned_data.get('telephone', '')
        self.instance.adresse = self.cleaned_data.get('adresse', '')
        self.instance.numeroUrgence = self.cleaned_data.get('numeroUrgence', '')
        self.instance.niveauEtude = self.cleaned_data.get('niveauEtude', '')
        self.instance.ecole = self.cleaned_data.get('ecole', '')
        self.instance.ner = self.cleaned_data.get('ner', '')
        self.instance.keri = self.cleaned_data.get('keri', '')
        self.instance.keribour = self.cleaned_data.get('keribour', '')
        self.instance.keriBa = self.cleaned_data.get('keriBa', '')
        self.instance.keribourBa = self.cleaned_data.get('keribourBa', '')
        self.instance.notes = self.cleaned_data.get('notes', '')
        
        if self.cleaned_data.get('photo'):
            self.instance.photo = self.cleaned_data['photo']
        
        if commit:
            self.instance.save()
        return self.instance


