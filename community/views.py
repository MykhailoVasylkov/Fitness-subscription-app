from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import CommunityMessage, CommunityPost
from .forms import CommunityPostForm

# Create your views here.


def community(request):
     """ 
     A view to return the community page, with community posts and messages.
     """
     community_posts = CommunityPost.objects.filter(approved=True).annotate(total_likes=Count('likes')).order_by("-created_on")
     community_messages = CommunityMessage.objects.order_by('-timestamp')[:10]

     user_posts = None
     if request.user.is_authenticated:
          user_posts = community_posts.filter(author=request.user)

     user_profile = None
     if request.user.is_authenticated:
          try:
               user_profile = request.user.userprofile
          except UserProfile.DoesNotExist:
               pass
     
     if request.method == 'POST':
          if not request.user.is_authenticated:
               messages.error(request, 'You must be logged in to submit a post.')
               return redirect('account_login') 
          
          form = CommunityPostForm(request.POST, request.FILES)
          if form.is_valid():
               post = form.save(commit=False)
               post.author = request.user
               post.save()
               messages.success(request, 'Post submitted!')
               return redirect('community')
          else:
               messages.error(request, 'Failed to submit post!')
     else:
          form = CommunityPostForm()

     context = {
          'community_messages': community_messages,
          'community_posts': community_posts,
          'user_posts': user_posts,
          'user_profile': user_profile,
          'form': form,
     }
     return render(request, 'community/community.html', context)