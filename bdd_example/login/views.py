from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_root(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                return HttpResponseRedirect(reverse('login_success'))
        return HttpResponseRedirect(reverse('login_fail'))
    return render(request, 'login_root.html')


def login_fail(request):
    return render(request, 'login_fail.html')


def login_success(request):
    return render(request, 'login_success.html')
