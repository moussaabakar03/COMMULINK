from django.db import models
from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils import timezone


class Annee(models.Model):
    debutAnnee = models.DateField()
    finAnnee = models.DateField()

    def __str__(self):
        return f"{self.debutAnnee}- {self.finAnnee}"

class Membre(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre')
    ]

    # Informations de base
    nom = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    prenom = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    sexe = models.CharField(max_length=1, choices=GENRE_CHOICES)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Adresse email"
    )
    telephone = models.CharField(max_length=20, blank=True, null=True)
    
    # Adresse
    adresse = models.TextField(blank=True, null=True)
    profession = models.CharField(max_length=50)
    numeroUrgence = models.CharField(max_length=20, blank=True, null=True)
    niveauEtude = models.CharField(max_length=20, blank=True, null=True)
    ecole = models.CharField(max_length=20, blank=True, null=True)


    
    # Informations supplémentaires
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_derniere_modification = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        upload_to='membres/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    
    # Métadonnées
    notes = models.TextField(blank=True, null=True, verbose_name="Remarques")


    # information sur l'identité
    ner = models.CharField(max_length=20, blank=True, null=True)
    keri = models.CharField(max_length=20, blank=True, null=True)
    keribour = models.CharField(max_length=20, blank=True, null=True)
    keriBa = models.CharField(max_length=20, blank=True, null=True)
    keribourBa = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}--- {self.ner}. {self.keri}"

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['nom', 'prenom']
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['email']),
        ]
    
    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenom}"


#--------------------ANNONCES ET PAYEMENTS--------------------------------
class Annonce(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    est_publie = models.BooleanField(default=False)
    # auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='annonces/', null=True, blank=True)

    def __str__(self):
        return self.titre





# Create your models here.
class TypeEvenement(models.Model):
    nom_type_evenement = models.CharField(max_length=100)
    description_type_evenement = models.TextField()
    image_type_evenement = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.nom_type_evenement
    
class Evenement(models.Model):
    
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE, related_name="evement", null=True)
    typeEvenement = models.ForeignKey (TypeEvenement, on_delete=models.CASCADE, related_name= 'evenement')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    dateHeure = models.DateTimeField(editable=False, auto_now_add=True)
    photo = models.ImageField(upload_to='evenements')
    prix = models.DecimalField(max_digits=10 ,decimal_places=2, default=0.0, null=True)
    est_publie = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.titre

class EvenementImage(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='evenements/images')


class EquipeDirigeante(models.Model):
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    lienFacebook = models.CharField(max_length=100)
    lienInstagram = models.CharField(max_length=100)
    lienTwitter = models.CharField(max_length=100)
    image = models.ImageField(upload_to='equipe')

class Temoingnage(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to='temoignage')
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name ='temoignage', null=True, blank=True)
    video = models.FileField(upload_to='videos/')





class Paiement(models.Model):
    STATUT_CHOICES = [
        ('payé', 'Payé'),
        ('non_payé', 'Non payé'),
        ('moitié_payé', 'Moitié payé'),
        ('avance', 'Avance'),
    ]
    
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    montant = models.IntegerField()
    date_paiement = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    preuve_paiement = models.FileField(upload_to='paiements/', null=True, blank=True)


    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.membre} - {self.evenement} - {self.statut}"
    
    
class Reinscription(models.Model):
    # STATUT_CHOICES = [
    #     ('actif', 'Actif'),
    #     ('inactif', 'Inactif'),
    #     ('suspendu', 'Suspendu'),
    #     ('en_attente', 'En attente de validation'),
    # ]
    
    # Relations principales
    membre = models.ForeignKey(
        Membre, 
        on_delete=models.CASCADE, 
        related_name='reinscriptions'
    )
    annee = models.ForeignKey(
        Annee, 
        on_delete=models.CASCADE, 
        related_name='reinscriptions'
    )
    
    # Informations susceptibles de changer chaque année
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    # profession = models.CharField(max_length=50)
    numeroUrgence = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Numéro d'urgence"
    )
   
    ecole = models.CharField(max_length=50, blank=True, null=True)
    niveauEtude = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Niveau d'étude"
    )
    filiere = models.CharField(max_length=150, blank=True, null= True)
    
    # Informations de statut et de suivi
    # statut = models.CharField(
    #     max_length=20, 
    #     choices=STATUT_CHOICES, 
    #     default='en_attente'
    # )
    
    date_reinscription = models.DateTimeField(auto_now_add=True)
    
    # date_validation = models.DateTimeField(null=True, blank=True)
    
    # Cotisation annuelle (optionnel)
    # cotisation_payee = models.BooleanField(default=False)
    # montant_cotisation = models.DecimalField(
    #     max_digits=10, 
    #     decimal_places=2, 
    #     default=0.0, 
    #     null=True, 
    #     blank=True
    # )
    # date_paiement_cotisation = models.DateTimeField(null=True, blank=True)
    
    # Photo mise à jour pour l'année (optionnel)
    photo_annuelle = models.ImageField(
        upload_to='reinscriptions/%Y/',
        blank=True,
        null=True,
        verbose_name="Photo de l'année"
    )
    
    # Notes spécifiques à l'année
    # notes_annuelles = models.TextField(
    #     blank=True, 
    #     null=True, 
    #     verbose_name="Notes pour cette année"
    # )
    
    # class Meta:
    #     verbose_name = "Réinscription"
    #     verbose_name_plural = "Réinscriptions"
    #     ordering = ['-annee', 'membre_nom', 'membre_prenom']
    #     # Empêche un membre d'avoir plusieurs inscriptions pour la même année
    #     unique_together = [['membre', 'annee']]
    #     indexes = [
    #         models.Index(fields=['annee', 'statut']),
    #         models.Index(fields=['membre', 'annee']),
    #     ]
    
    # def _str_(self):
    #     return f"{self.membre.nom_complet} - {self.annee} ({self.statut})"
    
    # @property
    # def est_actif(self):
    #     """Vérifie si le membre est actif pour cette année"""
    #     return self.statut == 'actif' and self.cotisation_payee
    
    # def save(self, *args, **kwargs):
    #     """Validation automatique si la cotisation est payée"""
    #     if self.cotisation_payee and not self.date_validation:
    #         self.date_validation = timezone.now()
    #         if self.statut == 'en_attente':
    #             self.statut = 'actif'
    #     super().save(*args, **kwargs)


