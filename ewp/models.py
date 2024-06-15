# ewp/models.py
from django.db import models
from django.contrib.auth.models import User, auth
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='pics', blank=True, null=True)
    user_type=models.CharField(max_length=100, blank=True, null=True, default="patient")

    def __str__(self):
        return self.user.username
    
class DoctorType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor_types=models.ManyToManyField(DoctorType, blank=True)
    experience = models.IntegerField(default=0)  
    rating = models.FloatField(default=0.0) 
    availability = models.CharField(max_length=100, default='Available')  
    def __str__(self):
        return f"Dr. {self.profile.user.username}"
    def get_doctor_details(self):
        if self.user_type == 'doctor':
            try:
                return self.doctor
            except Doctor.DoesNotExist:
                return None
        return None
    
class PreviousDiseases(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
       
class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    age=models.IntegerField(default=0)
    gender=models.CharField(max_length=100, default='male')
    previous_diseases=models.ManyToManyField(PreviousDiseases, blank=True)  
    def __str__(self):
        return self.profile.user.username
    
class Disease(models.Model):
    name = models.CharField(max_length=255)
    doctor_type = models.ForeignKey(DoctorType, on_delete=models.CASCADE)

class DiseaseTreatment(models.Model):
    disease_name = models.CharField(max_length=255)
    doctor_type = models.CharField(max_length=255)
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    gender = models.CharField(max_length=10)  
    treatment = models.TextField()
    medication = models.TextField()

    def __str__(self):
        return f"{self.disease_name} - {self.doctor_type}"
    

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason_for_visit = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"

    class Meta:
        unique_together = ['doctor', 'appointment_date']    