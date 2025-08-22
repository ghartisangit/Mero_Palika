from email.message import EmailMessage
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from accounts.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages ,auth
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from complaints.models import Ward

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from accounts.forms import RegistrationForm
from accounts.models import CustomUser

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .forms import RegistrationForm
from .models import CustomUser
from complaints.models import Ward


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Get cleaned data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            ward = form.cleaned_data['ward'] 
            username = email.split("@")[0]

            # Create user instance and set municipality via ward
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                user_type='user',
                ward=ward, 
                phone_number=phone_number,
                is_active=False  # inactive until email verification
            )
            user.set_password(password)
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request, 
                'Registration successful! Please check your email to activate your account.'
            )
            return redirect(f'/accounts/login/?command=verification&email={email}')

        else:
            # Form invalid
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/register.html', {'form': form})

    else:
        # GET request
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                request.session['frontend_login'] = True
                messages.success(request, 'You are now logged in.')

                # Redirect by user_type
                return redirect('welcome')
            
            else:
                messages.error(request, 'Account is not activated. Please verify your email.')
        else:
            messages.error(request, 'Invalid login credentials')
        return redirect('login')
    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Congratulations! Your account has been activated.')
        else:
            messages.info(request, 'Your account is already activated.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('register')
    
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    request.session.pop('frontend_login', None)
    messages.success(request, 'You are logged out.')
    return redirect('login') 


