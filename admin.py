from django.contrib import admin
from .models import CustomUser, Patient, Doctor, Appointments, Prescription, ChatMessage, VideoCall, SMSMessage, ContactMessage, AnonymousUser

# Register your models here.
admin.site.site_header = 'Telemedicine Solution Platform Administration'

# Custom admin class for CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'date_of_birth', 'phone_number' )
    list_filter = ('user_type',)
    search_fields = ('username', 'email')

# Custom admin class for Patient model
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'email')
    search_fields = ('user__username', 'user__email')

# Custom admin class for Doctor model
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'email', 'specialization')
    search_fields = ('user__username', 'user__email')

# Custom admin classes for other models
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('patient','doctor', 'date_time', 'reason')
    list_filter = ('date_time',)
    search_fields = ('patient__user__username', 'doctor__user__username')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'medication', 'prescription_file')
    list_filter = ('date_time',)
    search_fields = ('patient__user__username', 'doctor__user__username')

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message', 'date_time')
    search_fields = ('sender__username', 'recipient__username', 'message')

class VideoCallAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time')
    list_filter = ('date_time',)
    search_fields = ('patient__user__username', 'doctor__user__username')

class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message', 'date_time')
    search_fields = ('sender__username', 'recipient__username', 'message')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

class AnonymousUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')

# Register custom admin classes
admin.site.register(AnonymousUser, AnonymousUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointments, AppointmentsAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(VideoCall, VideoCallAdmin)
admin.site.register(SMSMessage, SMSMessageAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
