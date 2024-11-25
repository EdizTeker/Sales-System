from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from item.views import item_index
from django.contrib import messages
from .token import account_activation_token

from django. template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return HttpResponse("Hello")

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Activation link is invalid!")


    return redirect('item:index')

def activateEmail(request, user, to_email):

    mail_subject = "Activate your user account."
    message = render_to_string("accounts/activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),                             
        'protocol': 'https' if request.is_secure() else 'http'                       
        })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
        received activation link to confirm and complete the registration. Note : Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
    

def login_view(request):
    if request.user.is_authenticated:
        return redirect('item:index')
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('item:index')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Login'})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('item:index')
    else:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)

            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            #new_user = authenticate(username=user.username, email=user.email, password=password)
            #login(request, new_user)
            return redirect('item:index')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Register'})

@login_required
def logout_view(request):
    logout(request)
    return redirect('item:index')