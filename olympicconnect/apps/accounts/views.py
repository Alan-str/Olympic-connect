from django.contrib.auth import logout
from django.shortcuts import render, redirect
from allauth.account.views import LoginView, SignupView
from allauth.account.forms import LoginForm, SignupForm
from .forms import CustomLoginForm, CustomSignupForm
from django.urls import reverse



def custom_logout(request):
    logout(request)
    return redirect('account_login')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm

class CustomSignupView(SignupView):
    template_name = 'accounts/signup.html'
    form_class = CustomSignupForm

    def get_success_url(self):
        return redirect(reverse('account_login'))

    def form_valid(self, form):
        user = form.save(self.request)
        return redirect(self.get_success_url())
    
