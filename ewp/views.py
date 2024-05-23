from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Doctor,Patient
from django.contrib.auth.models import User, auth
from django.shortcuts import render, get_object_or_404
User = get_user_model()

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
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        user_type = request.POST['user_type']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username unavailable')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                user.save()
                profile_img = request.FILES.get('profileimage')
                
                profile = Profile.objects.create(user=user, img=profile_img, user_type=user_type)
                
                if user_type == 'doctor':
                    doctor_type = request.POST['doctor_type']
                    experience = request.POST['experience']
                    rating = request.POST['rating']
                    availability = request.POST['availability']
                    Doctor.objects.create(profile=profile, doctor_type=doctor_type, experience=experience, rating=rating, availability=availability)
                else:
                    Patient.objects.create(profile=profile)
                
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)
        user_profile.save()
    
    doctor_details = None
    if user_profile.user_type == 'doctor':
        try:
            doctor_details = Doctor.objects.get(profile=user_profile)
        except Doctor.DoesNotExist:
            pass

    context = {
        'profile': user_profile,
        'doctor_details': doctor_details
    }

    return render(request, 'profile.html', context)
   