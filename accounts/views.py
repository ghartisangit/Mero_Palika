from email.message import EmailMessage
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from accounts.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



from complaints.models import Ward

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            ward = form.cleaned_data['ward']      
            username = email.split("@")[0]

            # Create user
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                user_type='user',
                ward=ward
            )
            user.phone_number = phone_number
            user.is_active = False  
            user.save()

              # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)

        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegistrationForm()
        wards = Ward.objects.all()
        return render(request, 'accounts/register.html', {'form': form , 'wards': wards})


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
