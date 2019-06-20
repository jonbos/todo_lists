from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    text='<html><title>To-Do Lists</title></html>'
    return HttpResponse(text)
