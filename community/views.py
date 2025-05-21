from django.shortcuts import render, redirect, get_object_or_404
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


def edit_post(request, pk):
     """
     Edit an existing instance of model:`community.CommunityPost`.
     """
     post = get_object_or_404(CommunityPost, pk=pk, author=request.user)

     if request.method == 'POST':
          form = CommunityPostForm(request.POST, request.FILES, instance=post)

          if form.is_valid():
               # Delete image if user checks the box
               if 'remove_image' in request.POST and post.image:
                    post.image.delete(save=False)
                    post.image = None

               form.save()
               messages.success(request, 'Your post has been updated.')
               return redirect('community')
          else:
               messages.add_message(
                    request,
                    messages.ERROR,
                    'Error updating post!'
               )
          return redirect('community')
     else:
          form = CommunityPostForm(instance=post)

     return redirect('community')


def delete_post(request, pk):
    """
    Delete an existing instance of model:`community.CommunityPost`.

    """
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.method == "POST":
        if post.author == request.user:
            post.delete()
            messages.add_message(
                request, messages.SUCCESS,
                'Your post has been deleted.'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'Error deleting post!'
            )

    return redirect('community')
