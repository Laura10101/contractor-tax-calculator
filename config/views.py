from django.shortcuts import render
from django.contrib import admin

# Create your views here.
@admin.site.admin_view
def config(request):
    template = 'config/config.html'
    return render(request, template)