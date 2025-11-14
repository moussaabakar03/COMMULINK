from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Membre

# Configuration pour Utilisateur
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Ajouter 'role' aux champs existants
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôle', {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('role',)

# Configuration pour Membre
admin.site.register(Membre)

