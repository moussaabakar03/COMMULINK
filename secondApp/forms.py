from django import forms
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils import timezone
from .models import Annee, Membre

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur

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
    
    # Adresse et profession
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    profession = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    numeroUrgence = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    niveauEtude = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    ecole = forms.CharField(
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
    
    # Photo et notes
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def save(self, commit=True):
        # Créez une nouvelle instance de Membre avec les données du formulaire
        membre = Membre(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            sexe=self.cleaned_data['sexe'],
            email=self.cleaned_data['email'],
            telephone=self.cleaned_data['telephone'],
            adresse=self.cleaned_data['adresse'],
            profession=self.cleaned_data['profession'],
            numeroUrgence=self.cleaned_data['numeroUrgence'],
            niveauEtude=self.cleaned_data['niveauEtude'],
            ecole=self.cleaned_data['ecole'],
            ner=self.cleaned_data['ner'],
            keri=self.cleaned_data['keri'],
            keribour=self.cleaned_data['keribour'],
            keriBa=self.cleaned_data['keriBa'],
            keribourBa=self.cleaned_data['keribourBa'],
            notes=self.cleaned_data['notes'],
        )
        
        # Gestion séparée de la photo car c'est un fichier
        if 'photo' in self.files:
            membre.photo = self.files['photo']
        
        if commit:
            membre.save()
        return membre

      
    
    def update(self, membre):
        # Met à jour une instance existante de Membre
        membre.nom = self.cleaned_data['nom']
        membre.prenom = self.cleaned_data['prenom']
        membre.sexe = self.cleaned_data['sexe']
        membre.email = self.cleaned_data['email']
        membre.telephone = self.cleaned_data['telephone']
        membre.adresse = self.cleaned_data['adresse']
        membre.profession = self.cleaned_data['profession']
        membre.numeroUrgence = self.cleaned_data['numeroUrgence']
        membre.niveauEtude = self.cleaned_data['niveauEtude']
        membre.ecole = self.cleaned_data['ecole']
        membre.ner = self.cleaned_data['ner']
        membre.keri = self.cleaned_data['keri']
        membre.keribour = self.cleaned_data['keribour']
        membre.keriBa = self.cleaned_data['keriBa']
        membre.keribourBa = self.cleaned_data['keribourBa']
        membre.notes = self.cleaned_data['notes']
        
        if 'photo' in self.files:
            membre.photo = self.files['photo']
        
        membre.save()
        return membre


#--------------------------------ANNONCES----------------------------------
from .models import Annonce, Paiement

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
