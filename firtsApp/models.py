from django.db import models

# Create your models here.
class TypeEvenement(models.Model):
    nom_type_evenement = models.CharField(max_length=100)
    description_type_evenement = models.TextField()
    image_type_evenement = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.nom_type_evenement
    
class Evenement(models.Model):
    typeEvenement = models.ForeignKey (TypeEvenement, on_delete=models.CASCADE, related_name= 'evenement')
    # titre = models.CharField(max_length=200)
    description = models.TextField()
    dateHeure = models.DateTimeField(editable=False, auto_now_add=True)
    photo = models.ImageField(upload_to='evenements')
    prix = models.DecimalField(max_digits=10 ,decimal_places=2, default=0.0, null=True)
    
    
    def __str__(self):
        return self.typeEvenement.nom_type_evenement

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
