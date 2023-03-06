from django.shortcuts import render
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    return render(request, 'musicApp/index.html')

def search(request):
    pass