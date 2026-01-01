from django import forms
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils import timezone
from .models import Annee, Membre, Annonce, Paiement, RapportEvenement, Utilisateur


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import authenticate


class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'role')

class UtilisateurChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'role')

        
class MembreForm(forms.Form):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    
    NIVEAU_ETUDE_CHOICES = [
        ('', 'Sélectionnez votre niveau'),
        ('L1', 'L1 (Licence 1)'),
        ('L2', 'L2 (Licence 2)'),
        ('L3', 'L3 (Licence 3)'),
        ('M1', 'M1 (Master 1)'),
        ('M2', 'M2 (Master 2)'),
        ('Doctorat', 'Doctorat'),
    ]
    
    ECOLE_CHOICES = [
        ('', 'Sélectionnez votre établissement'),
        ('IPNET', 'IPNET'),
        ('Formatec', 'Formatec'),
        ('Esgis', 'Esgis'),
        ('Esac Nd', 'Esac Nd'),
        ('ESA', 'ESA'),
        ('Université de Lomé', 'Université de Lomé'),
        ('Université de Kara', 'Université de Kara'),
        ('Autre', 'Autre (précisez)'),
    ]

    # Informations de base
    nom = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    prenom = forms.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    sexe = forms.ChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    telephone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Adresse
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    # Identifiants de connexion
    nom_utilisateur = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choisissez un nom d\'utilisateur unique'
        })
    )
    
    mot_de_passe = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Créez un mot de passe sécurisé'
        })
    )
    
    # Informations académiques
    niveauEtude = forms.ChoiceField(
        choices=NIVEAU_ETUDE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    ecole = forms.ChoiceField(
        choices=ECOLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'ecole-select'  # ID personnalisé
        })
    )

    ecole_autre = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'ecole-autre-input',  # ID personnalisé
            'placeholder': 'Précisez le nom de votre établissement'
        })
    )
    
    filiere = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    numeroUrgence = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Informations sur l'identité
    ner = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    keri = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    keribour = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    keriBa = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    keribourBa = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    toute_info_sur_identite = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ajoutez toute information complémentaire concernant votre identité'
        })
    )
    
    # Photo et notes
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def clean(self):
        cleaned_data = super().clean()
        ecole = cleaned_data.get('ecole')
        ecole_autre = cleaned_data.get('ecole_autre')
        
        # Si "Autre" est sélectionné, le champ ecole_autre devient obligatoire
        if ecole == 'Autre' and not ecole_autre:
            raise forms.ValidationError("Veuillez préciser le nom de votre établissement.")
        
        return cleaned_data

    def save(self, commit=True):
        # Déterminer la valeur finale de l'école
        ecole_value = self.cleaned_data['ecole']
        if ecole_value == 'Autre':
            ecole_value = self.cleaned_data['ecole_autre']
        
        # Créez une nouvelle instance de Membre avec les données du formulaire
        membre = Membre(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            sexe=self.cleaned_data['sexe'],
            email=self.cleaned_data['email'],
            telephone=self.cleaned_data['telephone'],
            adresse=self.cleaned_data['adresse'],
            nom_utilisateur=self.cleaned_data['nom_utilisateur'],
            mot_de_passe=self.cleaned_data['mot_de_passe'],
            numeroUrgence=self.cleaned_data['numeroUrgence'],
            niveauEtude=self.cleaned_data['niveauEtude'],
            ecole=ecole_value,  # Utilise la valeur finale
            filiere=self.cleaned_data['filiere'],
            ner=self.cleaned_data['ner'],
            keri=self.cleaned_data['keri'],
            keribour=self.cleaned_data['keribour'],
            keriBa=self.cleaned_data['keriBa'],
            keribourBa=self.cleaned_data['keribourBa'],
            toute_info_sur_identite=self.cleaned_data['toute_info_sur_identite'],
            notes=self.cleaned_data['notes'],
        )
        
        # Gestion séparée de la photo car c'est un fichier
        if 'photo' in self.files:
            membre.photo = self.files['photo']
        
        if commit:
            membre.save()
        return membre

    def update(self, membre):
        # Déterminer la valeur finale de l'école
        ecole_value = self.cleaned_data['ecole']
        if ecole_value == 'Autre':
            ecole_value = self.cleaned_data['ecole_autre']
        
        # Met à jour une instance existante de Membre
        membre.nom = self.cleaned_data['nom']
        membre.prenom = self.cleaned_data['prenom']
        membre.sexe = self.cleaned_data['sexe']
        membre.email = self.cleaned_data['email']
        membre.telephone = self.cleaned_data['telephone']
        membre.adresse = self.cleaned_data['adresse']
        membre.nom_utilisateur = self.cleaned_data['nom_utilisateur']
        membre.mot_de_passe = self.cleaned_data['mot_de_passe']
        membre.numeroUrgence = self.cleaned_data['numeroUrgence']
        membre.niveauEtude = self.cleaned_data['niveauEtude']
        membre.ecole = ecole_value  # Utilise la valeur finale
        membre.filiere = self.cleaned_data['filiere']
        membre.ner = self.cleaned_data['ner']
        membre.keri = self.cleaned_data['keri']
        membre.keribour = self.cleaned_data['keribour']
        membre.keriBa = self.cleaned_data['keriBa']
        membre.keribourBa = self.cleaned_data['keribourBa']
        membre.toute_info_sur_identite = self.cleaned_data['toute_info_sur_identite']
        membre.notes = self.cleaned_data['notes']
        
        if 'photo' in self.files:
            membre.photo = self.files['photo']
        
        membre.save()
        return membre


#--------------------------------ANNONCES----------------------------------

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'contenu', 'image']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 5}),
        }

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'
        widgets = {
            'date_paiement': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        widgets = {
            'montant': forms.NumberInput(attrs={'min': '0', 'step': '25'}),
        }

class PaiementEvenementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        exclude = ['evenement']
        widgets = {
            'montant': forms.NumberInput(attrs={'min': '25', 'step': '25'}),
        }


class AnneeForm(forms.Form):
    debutAnnee = forms.DateField(label="Début Annee", widget=forms.TextInput(attrs={"type": "date"}))
    finAnnee = forms.DateField(label="Fin Annee", widget=forms.TextInput(attrs={"type": "date"}))
        
        

class ReinscriptionForm(forms.Form):
    username = forms.CharField(max_length=120, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    numeroUrgence = forms.CharField(max_length=120, required=False)
    telephone = forms.CharField(max_length=120, required=False)  
    adresse = forms.CharField(max_length=255, required=False)  
    ecole = forms.CharField(max_length=150, required=False)
    niveauEtude = forms.CharField(max_length=120, required=False)  
    filiere = forms.CharField(max_length=150, required=False)
    photo_annuelle = forms.ImageField(required=False)





class RapportEvenementForm(forms.ModelForm):
    class Meta:
        model = RapportEvenement
        fields = [
            'titre', 'resume', 'objectifs', 'deroulement',
            'points_positifs', 'points_a_ameliorer',
            'recommandations', 'nb_participants',
            'budget_prevu', 'budget_depense',
        ]
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre du rapport"
            }),
            'resume': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Résumé général de l'évènement"
            }),
            'objectifs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'deroulement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'points_positifs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'points_a_ameliorer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'recommandations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'nb_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'budget_prevu': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'budget_depense': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
        }
        
        
        
        
        
