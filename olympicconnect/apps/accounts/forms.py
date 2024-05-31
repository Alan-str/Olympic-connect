
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.utils.safestring import mark_safe


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Prénom')
    last_name = forms.CharField(max_length=30, label='Nom')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
class CustomLoginForm(LoginForm):
    # accept_privacy_policy = forms.BooleanField(
    #     label=mark_safe('Accepter les <a href="/politique-de-confidentialite/" target="_blank">politiques de confidentialité</a>'),
    #     required=True
    # )

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = "E-mail"
        self.fields['password'].label = "Mot de passe"