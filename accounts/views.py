from django.contrib.auth import login as auth_login
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from boards.models import UserGender


def signup(request):
    if request.method == 'POST':
        #form = UserCreationForm()
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            usergender = UserGender.objects.create(gender=form.cleaned_data.get('gender'),foruser=user)
            return redirect('home')
    else:
        #form = UserCreationForm()
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

