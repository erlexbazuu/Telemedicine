from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/', views.register_patient, name='register_patient'),
    path('doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('patientdashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('makeappointment/',views.make_appointment, name='make_appointment'),
    path('contact/', views.contact_us, name='contact_us'),
    path('requestappointment/',views.request_appointment, name='request_appointment'),
    path('update/doctor/', views.doctor_update_view, name='doctor_update_view'),
    path('patient/update/', views.patient_update_view, name='patient_update_view'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('deny-appointment/<int:appointment_id>/', views.deny_appointment, name='deny_appointment'),
    path('accept-anonymous-appointment/<int:appointment_id>/', views.accept_anonymous_appointment, name='accept_anonymous_appointment'),
    path('deny-anonymous-appointment/<int:appointment_id>/', views.deny_anonymous_appointment, name='deny_anonymous_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctors_by_specialization/<int:specialization_id>/', views.doctors_by_specialization, name='doctors_by_specialization'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/requests/', views.patient_appointments_requests, name='patient_appointments_requests'),
    

    #path('doctor/accept_appointment_request/<int:appointment_request_id>/', views.accept_appointment_request_view, name='accept_appointment_view'),
    #path('doctor/decline_appointment_request/<int:appointment_request_id>/', views.decline_appointment_request_view, name='decline_appointment_view'),
    #path('regular-user-appointment-request/', views.regular_user_appointment_request, name='regular_user_appointment_request'),
    #path('patient-appointment-request/', views.patient_appointment_request, name='patient_appointment_request'),

]

