from django.shortcuts import render

# Create your views here.

def index(request):
     """ A view to return the index page """
     
     return render(request, 'home/index.html')

def terms(request):
     """ A view to return the terms of use page """
     
     return render(request, 'home/terms_of_use.html')

def privacy(request):
     """ A view to return the privacy policy page """
     
     return render(request, 'home/privacy_policy.html')