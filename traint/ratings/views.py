from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.db import models
from .models import Dress


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