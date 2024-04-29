#from django.db import models
#from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

    

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True, help_text='Specific permissions for this user.')
    def __str__(self):
        return self.username
    



#Patient model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20, default='Unknown')
    last_name = models.CharField(max_length=20, default='Unknown')
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=False, default=None)
    email=models.EmailField(unique=True)
    # add any additional fields as needed

class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20, default='Unknown')
    last_name = models.CharField(max_length=20, default='Unknown')
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=False, default=None)  # Use DateField instead of Field
    email = models.EmailField(unique=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    medication = models.CharField(max_length=100)
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    # add any additional fields as needed

class VideoCall(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

class SMSMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_sms_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_sms_messages')
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
class AnonymousUser(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Appointments(models.Model):
    date_time = models.DateTimeField()
    reason = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    

    def __str__(self):
        return f"Appointment: {self.patient.user.username} - {self.doctor.user.username} - {self.date_time}"

class AnonymousAppointments(models.Model):
    anonymous_user_id = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)

class AppointmentStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    appointment = models.OneToOneField(Appointments, on_delete=models.CASCADE, related_name='status')

