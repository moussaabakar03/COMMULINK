from django.db import models
from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, Group, Permission



class Utilisateur(AbstractUser):
    ROLES = [  
        ("membreLambda", "Membre Lambda"),
        ("membreEquipe", "Membre de l'équipe")  
    ]
    
    groups = models.ManyToManyField( 
        Group, 
        related_name='utilisateur_groups', 
        blank=True, 
        help_text='The groups this user belongs to.', 
        verbose_name='groups'
    ) 
    
    user_permissions = models.ManyToManyField( 
        Permission, 
        related_name='utilisateur_user_permissions', 
        blank=True, 
        help_text='Specific permissions for this user.', 
        verbose_name='user permissions'
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLES,
        default="membreLambda",  # Valeur par défaut
        verbose_name="Rôle"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"  # Affiche le label lisible
    
    def est_membre_equipe(self):
        """Méthode helper pour vérifier le rôle"""
        return self.role == "membreEquipe"
    
    
    
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

    utilisateur = models.OneToOneField(Utilisateur, on_delete= models.CASCADE, null = True, blank= True, related_name= "membre")

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
    
    utilisateur = models.OneToOneField(Utilisateur, on_delete= models.CASCADE, null = True, blank= True, related_name= "equipeDirigeante")
    
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
    
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
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
    
    adresse = models.CharField(max_length=150, null = True, blank=True)
    date_reinscription = models.DateTimeField(auto_now_add=True)
    
    photo_annuelle = models.ImageField(
        upload_to='reinscriptions/%Y/',
        blank=True,
        null=True,
        verbose_name="Photo de l'année"
    )
    