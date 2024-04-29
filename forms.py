from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Patient, Doctor, Appointments, ContactMessage, Specialization, AnonymousUser, AnonymousAppointments
from datetime import *
from django.core.exceptions import ValidationError

#from .models import Record

class PatientSignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    first_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Your Email'}))
    phone_number=forms.CharField(label="", max_length= 20, required= True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    date_of_birth = forms.DateField(label="Date of Birth", required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type':'date','class':'form-control', 'placeholder':'Date of Birth'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(PatientSignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Your Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            patient=Patient.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
            patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    first_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    phone_number=forms.CharField(label="", max_length= 20, required= True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), empty_label="Select Specialization")
    date_of_birth = forms.DateField(label="Date of Birth", required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type':'date','class':'form-control', 'placeholder':'Date of Birth'}))


    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'specialization', 'date_of_birth', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(DoctorSignUpForm, self).__init__(*args, **kwargs) 

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            doctor=Doctor.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                specialization=self.cleaned_data['specialization'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
            doctor.save()
        return user

class AnonymousUserAppointmentRequestForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Last Name", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(label="Phone Number", max_length= 20, required= True, widget=forms.TextInput(attrs={'class':'form-control'}))
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=True)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), required=False)
    date_time=forms.DateTimeField(label="Date and Time", input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}))
    reason = forms.CharField(label="Reason", required=True, widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':50 , 'placeholder':'Reason for appointment...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.none()

        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['doctor'].queryset = Doctor.objects.filter(specialization_id=specialization_id).order_by('last_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif 'specialization' in self.initial:
            self.fields['doctor'].queryset = self.initial['specialization'].doctor_set.order_by('last_name')

    def save(self):
        # Create a new AnonymousUser entry
        anonymous_user = AnonymousUser.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            email=self.cleaned_data['email']
        )

        # Create a new Appointment entry
        appointment = AnonymousAppointments.objects.create(
            # Assuming the logged in user is the patient
            doctor=self.cleaned_data['doctor'],
            anonymous_user_id=anonymous_user,
            date_time=self.cleaned_data['date_time'],
            reason=self.cleaned_data['reason']
        )

        return appointment



class ContactForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=70, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}))
    email = forms.EmailField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    subject = forms.CharField(label="", max_length=50, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subject'}))
    message = forms.CharField(label="", max_length=400, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Message'}))
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class UpdatePatientForm(forms.ModelForm):
    first_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label="", max_length=40, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    phone_number = forms.CharField(label="", max_length=13, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    date_of_birth = forms.DateField(label="", required=True, input_formats=['%Y-%m-%d'], widget=forms.SelectDateWidget(attrs={'class':'form-control', 'placeholder':'Date of Birth'}))
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']


from django.forms import ModelChoiceField


class AppointmentRequestForm(forms.Form):
    specialization = ModelChoiceField(queryset=Specialization.objects.all(), required=True)
    doctor = ModelChoiceField(queryset=Doctor.objects.none(), required=False)
    date_time = forms.DateTimeField(label="Date and Time", input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}))
    reason = forms.CharField(label="Reason", required=True, widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':50 , 'placeholder':'Reason for appointment...'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.none()

        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['doctor'].queryset = Doctor.objects.filter(specialization_id=specialization_id).order_by('last_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif 'specialization' in self.initial:
            self.fields['doctor'].queryset = self.initial['specialization'].doctor_set.order_by('last_name')
    class Meta:
        model = Appointments
        fields = ['doctor', 'date_time', 'reason']

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']
  
from django import forms
from django.forms import ModelChoiceField
from .models import Doctor, Appointments

class AppointmentsRequestForm(forms.Form):
    specialization = ModelChoiceField(queryset=Specialization.objects.all(), required=True)
    doctor = ModelChoiceField(queryset=Doctor.objects.none(), required=False)
    date_time = forms.DateTimeField(label="Date and Time", input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}))
    reason = forms.CharField(label="Reason", required=True, widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':50 , 'placeholder':'Reason for appointment...'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.none()

        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['doctor'].queryset = Doctor.objects.filter(specialization_id=specialization_id).order_by('last_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif 'specialization' in self.initial:
            self.fields['doctor'].queryset = self.initial['specialization'].doctor_set.order_by('last_name')

from django import forms
from .models import Patient

# forms.py
from django import forms
from .models import Patient

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'phone_number']
class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'specialization']


