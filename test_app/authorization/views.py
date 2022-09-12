# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#basic-sign-up
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import SignUpForm
from business.models import Business
from .models import Roles
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.data['business'])
            if not Business.objects.filter(business_title=form.cleaned_data.get('business')).exists():
                #print(business)
                user = form.save(commit=False)
                business = Business(business_title=form.cleaned_data.get('business'))
                business.save()
                user.business = business
                user.role = "business_admin"
                user.save()
                print(user)
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                print(raw_password)
                user = authenticate(request=request,
                                    username=username,
                                    password=raw_password)
                print("User", user)
                login(request, user)
                return redirect('admin')
            else:
                form.add_error('business',
                 ValidationError(
                    _('Invalid value: %(value)s'),
                    code='invalid',
                    params={'value': '42'},
                ))


            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            if user.role in ['business_admin','business_manager']:
                redirect('/admin/business')
            else:
                return redirect('/admin')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('/admin')


    else:
        form = AuthenticationForm()
    return render(request, '/admin', {'form': form})
