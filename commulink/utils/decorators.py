from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser or request.user.role =="membreEquipe":
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Vous n\'avez pas les droits pour accéder à cette page')
        return redirect('connexion')  
    return wrapper

def membre_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role =="membreLambda" or request.user.role == "membreEquipe":
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Vous n\'avez pas les droits pour accéder à cette page')
        return redirect('connexion') 
    return wrapper


