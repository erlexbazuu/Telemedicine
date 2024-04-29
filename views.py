from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
import mysql.connector
from .forms import PatientSignUpForm, DoctorSignUpForm, AppointmentsRequestForm, ContactForm, UpdateDoctorForm, Specialization, AnonymousUserAppointmentRequestForm, PatientUpdateForm, AppointmentRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Appointments, Doctor, Patient, CustomUser, AnonymousUser, AnonymousAppointments, Prescription, Appointments, AppointmentStatus
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


from django.shortcuts import render, redirect
from .forms import AppointmentsRequestForm
from .models import Appointments



def doctors_by_specialization(request, specialization_id):
    doctors = Doctor.objects.filter(specialization_id=specialization_id)
    data = list(doctors.values('pk', 'first_name', 'last_name'))
    return JsonResponse(data, safe=False)


@login_required
def accept_appointment(request, appointment_id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointments, id=appointment_id, doctor=doctor)
    appointment.AppointmentStatus = 'accepted'
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def deny_appointment(request, appointment_id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointments, id=appointment_id, doctor=doctor)
    appointment.status = 'denied'
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def accept_anonymous_appointment(request, appointment_id):
    doctor = request.user.doctor
    appointment = get_object_or_404(AnonymousAppointments, id=appointment_id, doctor=doctor)
    appointment.status = 'accepted'
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def deny_anonymous_appointment(request, appointment_id):
    doctor = request.user.doctor
    appointment = get_object_or_404(AnonymousAppointments, id=appointment_id, doctor=doctor)
    appointment.status = 'denied'
    appointment.save()
    return redirect('doctor_dashboard')


@login_required
def patient_appointments_requests(request):
    # Get the logged-in patient object
    patient = get_object_or_404(Patient, user=request.user)

    # Retrieve all appointment requests for the patient
    appointments = Appointments.objects.filter(patient=patient)

    context = {
        'appointments': appointments,
    }

    return render(request, 'patient_appointment_requests.html', context)

@login_required
def doctor_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointments.objects.filter(doctor=doctor)
    anonymous_appointments = AnonymousAppointments.objects.filter(doctor=doctor)

    if request.method == 'POST':
        # Handle file upload for appointments
        for appointment in appointments:
            if f'prescription_{appointment.id}' in request.FILES:
                prescription_file = request.FILES[f'prescription_{appointment.id}']
                fs = FileSystemStorage()
                filename = fs.save(prescription_file.name, prescription_file)
                appointment.prescription.name = filename
                appointment.save()

        # Handle file upload for anonymous appointments
        for anonymous_appointment in anonymous_appointments:
            if f'anonymous_prescription_{anonymous_appointment.id}' in request.FILES:
                prescription_file = request.FILES[f'anonymous_prescription_{anonymous_appointment.id}']
                fs = FileSystemStorage()
                filename = fs.save(prescription_file.name, prescription_file)
                anonymous_appointment.prescription.name = filename
                anonymous_appointment.save()

    context = {
        'appointments': appointments,
        'anonymous_appointments': anonymous_appointments,
    }

    return render(request, 'doctor_appointments.html', context)

@login_required
def doctor_update_view(request):
    # Get the logged-in doctor object
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':
        form = UpdateDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message
            messages.success(request, "You have successfully updated your personal details!")
            return redirect('doctor_dashboard')  # Replace 'dashboard' with your desired URL name
    else:
        form = UpdateDoctorForm(instance=doctor)

    context = {
        'form': form
    }
    return render(request, 'doctor_update.html', context)

@login_required
def request_appointment(request):
    # Get the logged-in patient object
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        form = AppointmentsRequestForm(request.POST)
        if form.is_valid():
            # Create a new Appointment entry
            appointment = Appointments.objects.create(
                patient=patient,
                doctor=form.cleaned_data['doctor'],
                date_time=form.cleaned_data['date_time'],
                reason=form.cleaned_data['reason']
            )
            # Save the appointment to the database
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentsRequestForm()

    context = {
        'form': form,
        'patient_data': patient,
    }
    return render(request, 'patient_appointment_request.html', context)



@login_required
def patient_update_view(request):
    # Get the logged-in patient object
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message
            messages.success(request, "You have successfully updated your personal details!")
            return redirect('patient_dashboard')  # Replace 'dashboard' with your desired URL name
    else:
        form = PatientUpdateForm(instance=patient)

    context = {
        'form': form
    }
    return render(request, 'patient_update.html', context)



def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')  # Add success message
            return redirect('home')  # Redirect to the landing page after submission
    else:
        form = ContactForm()
    return render(request, 'landingpage.html', {'form': form})

from .models import AnonymousUser

def make_appointment(request):
    if request.method == 'POST':
        appointment_form = AnonymousUserAppointmentRequestForm(request.POST)

        if appointment_form.is_valid():
            appointment_form = appointment_form.save()

            messages.success(request, 'Your request has been submitted, you will receive feedback soon!')
            return redirect('make_appointment')  # Redirect to a success page after form submission
    else:
        appointment_form = AnonymousUserAppointmentRequestForm()

    return render(request, 'appointment.html', {'appointment_form':appointment_form})



def home(request):
    if request.user.is_authenticated:
        # Redirect to the respective dashboard if the user is logged in
        if request.user.user_type == 'patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'doctor':
            return redirect('doctor_dashboard')
    else:
        # Render the landing page if the user is not logged in
        # Add any context data that you want to pass to the template
        messages_to_display = messages.get_messages(request)
        context = {
            'messages': messages_to_display
        }
        # Render the landingpage.html template with the context data
        return render(request, 'landingpage.html', context)
    
    return render(request, 'landingpage.html')
    



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to the respective dashboard based on user type
            if user.user_type == 'patient':
                messages.success(request, "You Have Been Logged In as a Patient!")
                return redirect('patient_dashboard')
            elif user.user_type == 'doctor':
                messages.success(request, "You Have Been Logged In as Doctor!")
                return redirect('doctor_dashboard')
        else:
             messages.success(request, "There Was An Error Logging You In, Please Try Again...")
             return redirect('home')
            #pass
    else:
        # handle GET request
        pass
    # render login template
    return render(request, 'login.html')


#Log out user
def user_logout(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    # redirect to the landing page after logout
    return redirect('home')

def register_patient(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.user_type='patient'
            user.save()
            patient= Patient.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                email=user.email,
                date_of_birth=user.date_of_birth,
            )
            patient.save()
            # redirect to the login page after a successful sign-up
            messages.success(request, "You Have Successfully Registered as a Patient! Welcome!")
            return redirect('user_login')
    else:
        form = PatientSignUpForm()
    return render(request, 'register_patient.html', {'form': form})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'doctor'
            user.save()
            doctor = Doctor.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                specialization=form.cleaned_data['specialization'],
            )
            doctor.save()
            messages.success(request, "You have successfully registered as Doctor!")
            return redirect('user_login')
    else:
        form = DoctorSignUpForm()

    return render(request, 'register_doctor.html', {'form': form})


def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')




def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')



