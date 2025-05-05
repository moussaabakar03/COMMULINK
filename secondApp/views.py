from django.shortcuts import render


# DASHBOARD VIEW

def admin_dashboard(request):
    return render(request, "admin/index.html")
