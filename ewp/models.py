# ewp/models.py
from django.db import models
from django.contrib.auth.models import User, auth
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='pics', blank=True, null=True)
    user_type=models.CharField(max_length=100, blank=True, null=True, default="patient")

    def __str__(self):
        return self.user.username
class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor_type = models.CharField(max_length=100, blank=True, null=True)
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


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.profile.user.username