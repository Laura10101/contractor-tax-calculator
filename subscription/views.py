from django.shortcuts import render

# Create your views here.
def subscription(request):
    template = 'subscription/subscription.html'
    context = {
    }

    return render(request, template, context)