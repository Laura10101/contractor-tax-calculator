from django.shortcuts import render

# Create your views here.
def config(request):
    template = 'config/config.html'
    return render(request, template)