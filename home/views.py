from django.shortcuts import render

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

def admin_index(request):
    template = 'home/admin_index.html'
    context = {
    }

    return render(request, template, context)

def home(request):
    template = 'home/home.html'
    context = {
    }

    return render(request, template, context)