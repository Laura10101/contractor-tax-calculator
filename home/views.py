from django.shortcuts import render
from django.contrib import admin
from django.contrib.auth.decorators import login_required

# Create your views here
def index(request):
    template = 'home/index.html'
    context = {
    }

    return render(request, template, context)

def contractor_index(request):
    template = 'home/contractor_index.html'
    context = {
    }

    return render(request, template, context)

@admin.site.admin_view
def admin_index(request):
    template = 'home/admin_index.html'
    context = {
    }

    return render(request, template, context)

@login_required
def home(request):
    template = 'home/home.html'
    context = {
    }

    return render(request, template, context)