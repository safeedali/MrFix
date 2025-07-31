from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SchdeuleForm
from .models import Schedule, Bill, Customers, Appointment, Worker, Feedback


@login_required(login_url='login_view')
def worker_home(request):
    return render(request, 'workertemp/worker_home.html')


@login_required(login_url='login_view')
def schedule_add(request):
    form = SchdeuleForm()
    if request.method == 'POST':
        form = SchdeuleForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.employee = Worker.objects.get(user=request.user)
            form.save()
            messages.info(request, 'schedule added successful')
            return redirect('schedule_view')
    return render(request, 'workertemp/schedule_add.html', {'form': form})


@login_required(login_url='login_view')
def schedule_view(request):
    worker = request.user
    worker = Worker.objects.get(user=worker)
    print(worker)
    s = Schedule.objects.filter(employee=worker).distinct()
    print(s)
    context = {
        'schedule': s
    }
    return render(request, 'workertemp/schedule_view.html', context)


@login_required(login_url='login_view')
def schedule_update(request, id):
    s = Schedule.objects.get(id=id)
    if request.method == 'POST':
        form = SchdeuleForm(request.POST or None, instance=s)
        if form.is_valid():
            form.save()
            messages.info(request, 'schdeule updated')
            return redirect('schedule_views')
    else:
        form = SchdeuleForm(instance=s)
    return render(request, 'workertemp/schedule_update.html', {'form': form})


@login_required(login_url='login_view')
def schedule_delete(request, id):
    s = Schedule.objects.filter(id=id)
    if request.method == 'POST':
        s.delete()
        return redirect('schedule_view')




@login_required(login_url='login_view')
def view_payment_details_worker(request):
    worker = get_object_or_404(Worker, user=request.user)

    # Show appointments of this worker where status = Completed
    appointments = Appointment.objects.filter(worker=worker, status='Completed')

    return render(request, 'workertemp/view_payment_details.html', {'appointments': appointments})


# @login_required(login_url='login_view')
# def appointment_view_worker(request):
#     user = request.user
#     print(user)
#     worker = Worker.objects.get(user=user)
#     print(worker,"worker")
#     data=Schedule.objects.filter(employee=worker)
#     print(data)
#     return render(request, 'workertemp/appointment_view.html', {'data': data})

@login_required(login_url='login_view')
def appointment_view_worker(request):
    user = request.user
    worker = Worker.objects.get(user=user)
    
    # Fetching schedules with related appointments
    data = Schedule.objects.filter(employee=worker).prefetch_related('appointment_set')
    print(data,"data")
    
    appointments = []
    for schedule in data:
        appointment = Appointment.objects.filter(schedule=schedule).first()  # Assuming one appointment per schedule
        print(appointment,"appoint")
        appointments.append({
            "schedule": schedule,
            "status": appointment.status if appointment else None
        })
    
    return render(request, 'workertemp/appointment_view.html', {'appointments': appointments})



@login_required(login_url='login_view')
def worker_feedback_view(request):
    # Show feedback where the logged-in user is the target (worker)
    feedbacks = Feedback.objects.filter(about_user=request.user)

    return render(request, 'workertemp/view_feedback.html', {'feedbacks': feedbacks})




@login_required(login_url='login_view')
def Worker_appointment_view(request):
    c = Worker.objects.get(user=request.user)
    a = Appointment.objects.filter(worker=c)
    return render(request, 'workertemp/appointment_view.html', {'appointment': a})
