from django.shortcuts import render

# Create your views here
def index(request):
    template = 'home/index.html'
    context = {
    }

    return render(request, template, context)

def home(request):
    template = 'home/home.html'
    context = {
    }

    return render(request, template, context)