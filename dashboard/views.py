from django.shortcuts import render

# Create your views here.
def dashboard(request):
    template = 'dashboard/dashboard.html'
    context = {
    }

    return render(request, template, context)