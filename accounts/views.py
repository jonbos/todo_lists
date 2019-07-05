from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages, auth
from .models import Token
# Create your views here.


def send_login_email(request):

    token = Token.objects.create(email=request.POST['email'])
    url = request.build_absolute_uri(reverse('login') + "?token=" + str(token.uid))
    message_body=f"Use this link to log in:\n\n{url}"
    send_mail('Your login link for Superlists', message_body,
              'noreply@satno7.press', [request.POST['email']])

    messages.success(
        request, "Check your email, we've sent you a link you can use to log in.")
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
