from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Doctor,Patient,DoctorType, Disease, DiseaseTreatment, Appointment
from django.contrib.auth.models import User, auth
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, get_object_or_404
User = get_user_model()

def index(request):
    return render(request, 'index.html')

def doctors(request):
    return render(request, 'doctors.html')

def chatbot(request):
    if request.method=="GET":
         return render(request, 'chatbot.html')
    else:
        disease_name = request.POST['disease_name']
        gender=request.POST['gender']
        try:
            disease = Disease.objects.get(name=disease_name)
            treatement= DiseaseTreatment.objects.get(disease_name=disease_name,gender=gender)
            doctor_type = disease.doctor_type
            doctors = Doctor.objects.filter(doctor_types=doctor_type)

            context = {
                'doctors': doctors,
                'disease_name': disease_name,
                'treatment': treatement,
                
            }
            return render(request, 'chatbot.html', context)
        except Disease.DoesNotExist or DiseaseTreatment.DoesNotExist:
            if Disease.DoesNotExist and DiseaseTreatment.DoesNotExist:
                 context={
                    'message':  'No Treatements and doctors found for the specified disease we will update you soon!!'
                }
            elif Disease.DoesNotExist:
                context={
                    'message': 'No doctors found for the specified disease'
                }
            elif DiseaseTreatment.DoesNotExist:
                context={
                    'message':  'No Treatements found for the specified disease we will update you soon!!'
                }
            else:
                context = {
                    'message':  'No data found'
                }
                   
            return render(request,'chatbot.html',context)


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
                    experience = request.POST['experience']
                    rating = request.POST['rating']
                    availability = request.POST['availability']
                    doctor=Doctor.objects.create(profile=profile, experience=experience, rating=rating, availability=availability)
                    doctor_type_ids = request.POST.getlist('doctor_types')
                    for doctor_type_id in doctor_type_ids:
                        doctor_type = DoctorType.objects.get(id=doctor_type_id)
                        doctor.doctor_types.add(doctor_type)
                    doctor.save()
                else:
                    age=request.POST['age']
                    gender=request.POST['gender']
                    Patient.objects.create(profile=profile,age=age,gender=gender)
                
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    else:
        doctor_types = DoctorType.objects.all()
        return render(request, 'register.html', {'doctor_types': doctor_types})
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request):
    try:
        # Get or create the user profile
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        # Initialize context
        context = {
            'profile': user_profile,
            'doctor_details': None,
            'doctor_types': None,
            'appointments': None
        }

        # If the user is a doctor, get doctor details and types
        if user_profile.user_type == 'doctor':
            try:
                doctor_details = Doctor.objects.get(profile=user_profile)
                doctor_types = doctor_details.doctor_types.all()
                context['doctor_details'] = doctor_details
                context['doctor_types'] = doctor_types
            except Doctor.DoesNotExist:
                pass

        # If the user is a patient, get patient details and appointments
        if user_profile.user_type == 'patient':
            try:
                patient = Patient.objects.get(profile=user_profile)
                appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
                context['appointments'] = appointments
            except Patient.DoesNotExist:
                pass

        return render(request, 'profile.html', context)

    except ObjectDoesNotExist:
        # If any profile fetching operation fails, handle it here
        return render(request, 'profile.html', {'profile': None, 'error': 'Profile not found'})


    try:
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
        doctor_profile = user_profile.doctor
        doctor_types = doctor_profile.doctor_types.all()
        profile = Profile.objects.get(user=request.user)
        patient = Patient.objects.get(profile=profile)
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
        context = {
            'profile': user_profile,
            'doctor_details': doctor_details,
            'doctor_types': doctor_types,
            'appointments': appointments
        }

        return render(request, 'profile.html', context)
    except ObjectDoesNotExist:
        user_profile = Profile.objects.get(user=request.user)
        return render(request, 'profile.html',{'profile': user_profile})
@login_required
def appointment(request):
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')
        disease_name = request.GET.get('disease_name')
        
        if not doctor_id or not disease_name:
            return HttpResponseBadRequest("Missing required parameters.")
        
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return HttpResponseBadRequest("Doctor not found.")
        
        context = {
            'doctor': doctor,
            'disease_name': disease_name,
        }
        return render(request, 'appointment.html', context)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        appointment_date = request.POST.get('appointment_date')
        reason_for_visit = request.POST.get('reason_for_visit')
        doctor = Doctor.objects.get(pk=doctor_id)

        if not appointment_date:
            return HttpResponseBadRequest("Invalid date/time format.")

        # Get the patient's profile and then the patient object
        try:
            profile = Profile.objects.get(user=request.user)
            patient = Patient.objects.get(profile=profile)
        except (Profile.DoesNotExist, Patient.DoesNotExist):
            return HttpResponseBadRequest("Patient not found.")

        # Check for overlapping appointments
        overlapping_appointments = Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date)
        if overlapping_appointments.exists():
            context = {
                'doctor': doctor,
                'disease_name': request.POST.get('disease_name'),
                'message': 'This doctor already has an appointment at the selected date and time. Please choose a different time.',
            }
            return render(request, 'appointment.html', context)

        # Create the appointment
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            reason_for_visit=reason_for_visit
        )
        appointment.save()

        return render(request, 'chatbot.html', context={'success':"Appointment Booked"})
