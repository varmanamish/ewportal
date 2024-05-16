from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def doctors(request):
    return render(request, 'doctors.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def departments(request):
    return render(request, 'departments.html')

def elements(request):
    return render(request, 'elements.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')