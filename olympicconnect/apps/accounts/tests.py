from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.accounts.forms import CustomSignupForm, CustomLoginForm

User = get_user_model()

# --- TESTS POUR LES MODÈLES ---
class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@exemple.com",
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.email, "test@exemple.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_security_key_generation(self):
        user = User.objects.create_user(
            email="keytest@exemple.com",
            password="securepassword123",
            first_name="Jane",
            last_name="Doe"
        )
        self.assertIsNotNone(user.security_key)
        self.assertEqual(len(user.security_key), 7)

    def test_custom_user_str_representation(self):
        user = User.objects.create_user(
            email="struser@exemple.com",
            password="password123"
        )
        self.assertEqual(str(user), "struser@exemple.com")

# --- TESTS POUR LES FORMULAIRES ---
class CustomSignupFormTest(TestCase):
    def test_valid_signup_form(self):
        form_data = {
            "email": "validuser@exemple.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "first_name": "Valid",
            "last_name": "User"
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        form_data = {
            "email": "invaliduser@exemple.com",
            "password1": "securepassword123",
            "password2": "wrongpassword",
            "first_name": "Invalid",
            "last_name": "User"
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

class CustomLoginFormTest(TestCase):
    def test_login_form_labels(self):
        form = CustomLoginForm()
        self.assertEqual(form.fields["login"].label, "E-mail")
        self.assertEqual(form.fields["password"].label, "Mot de passe")

# --- TESTS POUR LES VUES ---
class CustomLoginViewTest(TestCase):
    def test_login_view_get(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

class CustomSignupViewTest(TestCase):
    def test_signup_view_get(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_form_submission(self):
        response = self.client.post(reverse("account_signup"), data={
            "email": "newuser@exemple.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "first_name": "New",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(User.objects.filter(email="newuser@exemple.com").exists())

class CustomLogoutViewTest(TestCase):
    def test_logout_view(self):
        user = User.objects.create_user(email="logoutuser@exemple.com", password="password123")
        self.client.login(email="logoutuser@exemple.com", password="password123")
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)  # Redirection après déconnexion
        self.assertRedirects(response, reverse("account_login"))
