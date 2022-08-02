from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>The Munro Step Team Challenge, 2022</h1>")
