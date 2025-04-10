from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_admin:
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'user_dashboard.html')
