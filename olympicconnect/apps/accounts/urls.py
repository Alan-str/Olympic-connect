from django.urls import path, include
from .views import CustomLoginView, CustomSignupView

urlpatterns = [
    # path('', include('allauth.urls')),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),

]