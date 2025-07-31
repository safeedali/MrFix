from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Nurse, NurseBooking, Feedback


def nurseHome(request):
    return render(request,'nursetemp/nurseHome.html')





@login_required(login_url='login_view')
def nurse_appointment_view(request):
    nurse = Nurse.objects.get(login=request.user)
    bookings = NurseBooking.objects.filter(nurse=nurse, status='Accepted')
    return render(request, 'nursetemp/my_appointments.html', {'bookings': bookings})



@login_required(login_url='login_view')
def view_my_feedback_nurse(request):
    nurse = Nurse.objects.get(login=request.user)

    feedbacks = Feedback.objects.filter(about_user=request.user)

    return render(request, 'nursetemp/view_feedback.html', {'feedbacks': feedbacks})


@login_required
def nurse_view_payments(request):
    nurse = Nurse.objects.get(login=request.user)  # Correct lookup
    bookings = NurseBooking.objects.filter(nurse=nurse).order_by('-date')
    return render(request, 'nursetemp/nurse_view_payments.html', {'bookings': bookings})
