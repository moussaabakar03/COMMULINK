from secondApp.models import EquipeDirigeante

def membreConnecte(request):
    membre = None

    if request.user.is_authenticated:
        membre = EquipeDirigeante.objects.filter(
            utilisateur=request.user
        ).first()

    return {
        "membreEquipe": membre
    }
