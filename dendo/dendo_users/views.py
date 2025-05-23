from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponse

from .forms import LogInForm, PasswordUpdateForm, SignUpForm, UserEditForm
from .models import CustomUser
from .utils import UserHelper


# Create your views here.

HOME_PAGE_URL = 'dendo_users:test_page'

def test_view(request):
    return HttpResponse('Test Page')

@login_required
def logout_view(request):
    logout(request)
    return redirect(HOME_PAGE_URL)

class LoginView(FormView):
    template_name = 'dendo_users/login.html'
    form_class = LogInForm
    success_url = reverse_lazy(HOME_PAGE_URL)

    def form_valid(self, form):
        username_or_email = form.cleaned_data.get('username_or_email')
        password = form.cleaned_data.get('password')
        user = UserHelper.login_user(self.request, username_or_email, password)

        return super().form_valid(form)

class SignupView(FormView):
    template_name = 'dendo_users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy(HOME_PAGE_URL)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = UserHelper.create_user(
            self.request,
            username,
            email,
            password
        )
        return super().form_valid(form)

class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'dendo_users/editprofile.html'
    form_class = UserEditForm

    raise_exception = False

    def test_func(self):
        username = self.kwargs.get('username')
        user = UserHelper.get_user(username)
        return self.request.user == user

    def handle_no_permission(self):
        return redirect(self.request.META.get('HTTP_REFERER', HOME_PAGE_URL))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('dendo_users:user_page', kwargs={'username': self.kwargs.get('username')})

class UpdatePasswordView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'dendo_users/resetpassword.html'
    form_class = PasswordUpdateForm

    raise_exception = False

    def test_func(self):
        username = self.kwargs.get('username')
        user = UserHelper.get_user(username)
        return self.request.user == user
    
    def handle_no_permission(self):
        return redirect(self.request.META.get('HTTP_REFERER', HOME_PAGE_URL))

    def get_form_kwargs(self): 
        kwargs = super().get_form_kwargs()
        kwargs['current_password_hash'] = self.request.user.password

        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data.get('new_password')

        response = UserHelper.update_password(user, new_password)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('dendo_users:user_page', kwargs={'username': self.request.user.username})

class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'dendo_users/userprofile.html'
    slug_field = "username"
    slug_url_kwarg = "username"