from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ReviewForm
from django.urls import reverse
from django.db import models
from .models import Dress, Rating, Cluster
from django.db.models import Avg
from .suggestions import update_clusters
from django.contrib.auth.models import User
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def dress_list(request):
    dress_query_set = Dress.objects.order_by('-created_at')
    dress_list = list(dress_query_set)
    n = 3
    dress_table = [dress_list[i:i+n] for i in range(0, len(dress_list), n)]
    context = {'rows': dress_table}
    return render(request, 'ratings/dress_table.html', context)

def dress_detail(request, dress_id):
    dress = get_object_or_404(Dress, pk=dress_id)
    return render(request, 'ratings/dress_detail.html', {'dress': dress})


def add_rating(request, dress_id):
    dress = get_object_or_404(Dress, pk=dress_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = Rating()
        rating.rating = form.cleaned_data['rating']
        rating.user_name = request.user.username
        rating.dress = dress
        rating.save()
        return HttpResponseRedirect(reverse('ratings:dress_detail', args=(dress.id,)))
    return render(request, 'ratings/dress_detail.html', {'dress': dress, 'form': form})



# credit: https://www.codementor.io/jadianes/build-data-products-django-machine-learning-clustering-user-preferences-du107s5mk
def user_recommendation_list(request):
     # get this user's ratings
    user_ratings = Rating.objects.filter(user_name=request.user.username).prefetch_related('dress')
     # from the ratings, get a set of dress IDs
    user_ratings_dress_ids = set(map(lambda x: x.dress.id, user_ratings))
    try:
        user_cluster = \
            User.objects.get(username=request.user.username).cluster_set.first()
        if not user_cluster:
            dress_query_set = Dress.objects.order_by('-created_at')
            dress_list = list(dress_query_set)
            n = 3
            dress_table = [dress_list[i:i+n] for i in range(0, len(dress_list), n)]
            context = {'rows': dress_table}
            return render(request, 'ratings/dress_table.html', context)
        user_cluster_name = user_cluster.name
    except: # if no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name # first one for now
     # then get a dress list excluding the previous IDs 
    user_cluster_other_members = \
            Cluster.objects.get(name=user_cluster_name).users \
                .exclude(username=request.user.username).all() # other users except the current one
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))
    print(other_members_usernames)
    other_users_ratings = \
        Rating.objects.filter(user_name__in=other_members_usernames) \
            .exclude(dress__id__in=user_ratings_dress_ids)
    other_users_ratings_dress_ids = set(map(lambda x: x.dress.id, other_users_ratings))
    print(list(other_users_ratings_dress_ids))
    dress_list = sorted(
        list(Dress.objects.filter(id__in=other_users_ratings_dress_ids)), 
        key=lambda x: x.avg_rating(), 
        reverse=True
    )

    dress_list = sorted(
        list(Dress.objects.filter(id__in=other_users_ratings_dress_ids)), 
        key=lambda x: x.avg_rating(), 
        reverse=True
    )
    print(dress_list)
    n = 3
    dress_table = [dress_list[i:i+n] for i in range(0, len(dress_list), n)]
    context = {'rows': dress_table}
    return render(request, 'ratings/dress_table.html', context)