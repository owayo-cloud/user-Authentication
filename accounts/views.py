from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import MyUser
from .forms import RegisterForm, LoginForm, CustomSetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView,DetailView, UpdateView,DeleteView



def register_view(request):
    """
    Handles user registration.
    On GET request, it renders the registration template.
    On POST request, it validates the form data, creates a new user and logs them in.
    If the form is not valid, it returns a JSON response with the status 'error' and the form errors.
    On successful registration, it returns a JSON response with the status 'success'.
    """
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            next_url = request.POST.get('next', '/')
            return JsonResponse({'status': 'success',"next_url":next_url})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'base_form.html', {"next_url":next_url})



def login_view(request):
    """
    Handles user login.
    On GET request, it renders the login template.
    On POST request, it validates the form data and logs them in.
    If the form is not valid, it returns a JSON response with the status 'error' and the form errors.
    On successful login, it returns a JSON response with the status 'success'.
    """
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', '/')
                return JsonResponse({'status': 'success',"next_url":next_url})
            else:
                form.add_error(None, "Invalid email or password")

        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'base_form.html', {"next_url":next_url})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')


def profile(request):
    return render(request, 'profiles.html', {})

def users(request):
    context = {}
    context['users'] = MyUser.objects.exclude(id=request.user.id)
    return render(request, 'users.html', context)

class UsersCreateView(LoginRequiredMixin, CreateView):
    model = MyUser
    fields = ['first_name', 'last_name','username', 'email', 'password']
    template_name = 'new_user.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        role = self.request.POST.get('role')
        if role == 'manager':
            form.instance.is_staff = True
            form.instance.is_hr = False
        elif role == 'hr':
            form.instance.is_staff = False
            form.instance.is_hr = True
        return super().form_valid(form)
    
class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'new_user.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        role = self.request.POST.get('role')
        if role == 'manager':
            form.instance.is_staff = True
            form.instance.is_hr = False
        elif role == 'hr':
            form.instance.is_staff = False
            form.instance.is_hr = True
        return super().form_valid(form)
    
# user detail 
class UsersDetailView(LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = 'user_detail.html'
    
# user delete
class UsersDeleteView(LoginRequiredMixin, DeleteView):
    model = MyUser
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users')


class MyPasswordResetView(PasswordResetView):
    template_name = 'my_password_reset_form.html'
    email_template_name = 'my_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = MyUser.objects.get(email=email)
            return super().form_valid(form)
        except MyUser.DoesNotExist:
            messages.warning(self.request, 'No user found with this email')
            return self.form_invalid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'my_password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'my_password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    post_reset_login = True

    def form_valid(self, form):
        print("valid")
        form.save()
        return super().form_valid(form)


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'my_password_reset_complete.html'