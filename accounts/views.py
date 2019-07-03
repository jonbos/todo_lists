from django.shortcuts import redirect
from django.core.mail import send_mail

# Create your views here.


def send_login_email(request):
    send_mail('Your login link for Superlists', 'message', 'noreply@satno7.press', [request.POST['email']])
    return redirect('/')
