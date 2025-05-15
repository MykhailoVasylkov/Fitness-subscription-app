from django.shortcuts import render

# Create your views here.

def community(request):
     """ A view to return the community page """
     
     return render(request, 'community/community.html')