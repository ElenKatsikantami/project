# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, View, DeleteView
from django.shortcuts import get_object_or_404, redirect, reverse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, User_Edit_Form


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/project")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class user_list(LoginRequiredMixin,ListView):
    template_name = 'pages/user/users.html'

    def get_queryset(self):
        users = User.objects.all()
        return users

class edit_user(LoginRequiredMixin, UpdateView):
    template_name = 'pages/user/profile.html'
    form_class = User_Edit_Form

    def form_valid(self, form):
        form.save(commit=True)
        return redirect(reverse("user_list"))

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class delete_user(LoginRequiredMixin, DeleteView):
    model = User
    success_url ="/users"
    template_name = "pages/user/delete.html"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
