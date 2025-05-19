from django.shortcuts import render
from .models import CommunityMessage

# Create your views here.

def community(request):
     """ A view to return the community page """
     
     сommunity_messages = CommunityMessage.objects.order_by('-timestamp')[:10]
     return render(request, 'community/community.html', {'сommunity_messages': сommunity_messages})