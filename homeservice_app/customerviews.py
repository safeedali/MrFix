from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .forms import FeedbackForm, PayBillForm,ComplaintsForm,NurseBookingForm
from .models import Worker, Schedule, Customers, Appointment, Feedback, Bill, CreditCard, Work, Complaints, Nurse, \
    NurseBooking, Product
from .models import Feedback, Login, Worker, Nurse,NurseBookingPayment
from django.utils import timezone
@login_required(login_url='login_view')
def customer_home(request):
    Services  = Work.objects.all()
    print(f"SERVICES========================",Services)
    return render(request, 'customertemp/customer_home.html',{'Services':Services})


@login_required(login_url='login_view')
def view_workers_customer(request):
    data = Worker.objects.all()
    return render(request, 'customertemp/workers.html', {'data': data})


@login_required(login_url='login_view')
def view_schedule_customer(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    schedules = Schedule.objects.filter(employee__work_type=work).select_related('employee')
    context = {'work': work, 'schedules': schedules}
    return render(request, 'customertemp/schedule_view.html', context)




def view_schedule_customer(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    schedules = Schedule.objects.filter(employee__work_type=work).select_related('employee')

    customer = get_object_or_404(Customers, user=request.user)
    customer_appointments = Appointment.objects.filter(customer=customer)

    appointments_by_schedule = {a.schedule_id: a for a in customer_appointments}

    context = {
        'work': work,
        'schedules': schedules,
        'appointments_by_schedule': appointments_by_schedule
    }
    return render(request, 'customertemp/schedule_view.html', context)


@login_required

def book_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    customer = get_object_or_404(Customers, user=request.user)
    existing = Appointment.objects.filter(customer=customer, schedule=schedule).first()
    if not existing:
        # Fetch the charge from related work via the worker
        amount = schedule.employee.work_type.charge

        Appointment.objects.create(
            customer=customer,
            worker=schedule.employee,
            schedule=schedule,
            amount=amount,
            status=0,
            Approvel_status=0
        )

    return redirect('view_schedule_customer', work_id=schedule.employee.work_type.id)



# @login_required(login_url='login_view')
# def take_appointment(request, id):
#     s = Schedule.objects.get(id=id)  # Fetch the schedule
#     c = Customers.objects.get(user=request.user)  # Fetch the customer
#     appointment = Appointment.objects.filter(user=c, schedule=s)
#
#     if appointment.exists():
#         messages.info(request, 'You Have Already Requested Appointment for this Schedule')
#         return redirect('view_schedule')
#
#     if request.method == 'POST':
#         obj = Appointment()
#         obj.user = c
#         obj.schedule = s
#         obj.user2 = s.employee  # Assuming Schedule has a ForeignKey to Worker
#         obj.save()
#         messages.info(request, 'Appointment Booked Successfully')
#         return redirect('appointment_view')
#
#     return render(request, 'customertemp/take_appointment.html', {'schedule': s})




@login_required(login_url='login_view')
def Feedback_view_user(request):
    f = Feedback.objects.filter(user=request.user)
    return render(request, 'customertemp/complaint_view.html', {'feedback': f})


@login_required
def view_bill_user(request):
    customer = get_object_or_404(Customers, user=request.user)
    bills = Bill.objects.filter(name=customer).order_by('-bill_date')

    total_pending = sum(b.amount for b in bills if b.status == 0)

    context = {
        'bills': bills,
        'total_pending': total_pending
    }
    return render(request, 'customertemp/view_bill_user.html', context)







def pay_bill(request, bill_id):
    customer = get_object_or_404(Customers, user=request.user)
    bill = get_object_or_404(Bill, id=bill_id, name=customer)

    if request.method == "POST":
        bill.status = 1  # Mark bill as Paid
        bill.save()

        messages.success(request, "Payment Completed Successfully!")
        return redirect('customer_home')  # Change to your home page URL name

    return render(request, 'customertemp/pay_bill.html', {'bill': bill})


def pay_in_direct(request, id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    messages.info(request, 'Choosed to Pay Fee Direct in office')
    return redirect('bill_history')


def bill_history(request):
    u = Customers.objects.get(user=request.user)
    bill = Bill.objects.filter(name=u, status__in=[1, 2])

    return render(request, 'customertemp/view_bill_history.html', {'bills': bill})



def View_Services(request):
    Services = Work.objects.all()
    return render(request,'customertemp/View_Services.html', {'Services': Services})


def Complaints_add_user(request):
    form = ComplaintsForm()
    u = request.user
    if request.method == 'POST':
        form = ComplaintsForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u  # make sure 'u' is of type Login if using a custom model
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('customer_home')
    return render(request, 'customertemp/complaint_add.html', {'Complaints': form})




def complaint_reply_view(request):
    user = request.user
    complaints = Complaints.objects.filter(user=user, reply__isnull=False)
    return render(request, 'customertemp/complaint_reply.html', {'complaints': complaints})


def view_nurses(request):
    nurses = Nurse.objects.filter(approved=True)
    return render(request, 'customertemp/view_nurses.html', {'nurses': nurses})


def book_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    customer = Customers.objects.get(user=request.user)
    if request.method == 'POST':
        form = NurseBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.nurse = nurse
            booking.customer = customer
            booking.save()
            messages.success(request, 'Nurse booked successfully!')
            return redirect('view_my_bookings')
    else:
        form = NurseBookingForm()

    return render(request, 'customertemp/book_nurse.html', {'form': form, 'nurse': nurse})



def view_my_bookings(request):
    customer = Customers.objects.get(user=request.user)
    bookings = NurseBooking.objects.filter(customer=customer)
    return render(request, 'customertemp/view_my_bookings.html', {'bookings': bookings})

@login_required(login_url='login_view')
def book_appointment(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    user = request.user
    customer = get_object_or_404(Customers, user=request.user)
    worker = schedule.employee
    charge = worker.work_type.charge  # Get the charge from Work model

    # Optional: Prevent duplicate booking
    existing = Appointment.objects.filter(schedule=schedule, customer=customer).first()
    if existing:
        return redirect('appointment_already_exists')

    # Save booking with amount
    appointment = Appointment.objects.create(
        customer=customer,
        schedule=schedule,
        worker=worker,
        amount=charge,
        status='Pending'
    )

    # Pass booking details to the success page
    return render(request, 'customertemp/appointment_success.html', {
        'appointment': appointment
    })


@login_required
def view_my_appointments(request):
    customer = get_object_or_404(Customers, user=request.user)
    appointments = Appointment.objects.filter(customer=customer, status=1)
    return render(request, 'customertemp/my_appointments.html', {'appointments': appointments})

def prod_cus(request):
    products = Product.objects.all()
    return render(request,'customertemp/prod_cus.html',{'products':products})




def approve_WorkK(request, id):
    workk = Appointment.objects.get(id=id)
    workk.approval_status = 1
    workk.save()
    return redirect('view_my_appointments')



@login_required(login_url='login_view')
def Myappointment_view(request):
    c = Customers.objects.get(user=request.user)
    a = Appointment.objects.filter(customer=c)
    return render(request, 'customertemp/appointment_view.html', {'appointment': a})


@login_required(login_url='login_view')
def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.customer.user != request.user:
        return redirect('Myappointment_view')  # Security check: only the customer can pay
    if request.method == 'POST':
        # Here you can integrate real payment gateway logic, for now, just mark as paid
        appointment.status = 'Confirmed'  # Assuming 'Confirmed' means paid/approved
        print(">>>>>>>>>>>>>>",appointment.status)
        appointment.Approvel_status = True
        appointment.save()
        return redirect('Myappointment_view')
    return render(request, 'customertemp/payment_page.html', {'appointment': appointment})



@login_required(login_url='login_view')
def give_feedback(request, about_user_id):
    # Get the Login record of the person receiving feedback
    about_user = get_object_or_404(Login, id=about_user_id)
    customer = get_object_or_404(Customers, user=request.user)

    # Fetch all appointments of this customer
    appointments = Appointment.objects.filter(customer=customer).select_related('worker', 'schedule')

    # Pass appointments to the template

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user               # The customer giving feedback
            fb.about_user = about_user           # The worker/nurse receiving feedback
            fb.save()
            return redirect('customer_home')  # Redirect after successful feedback
    else:
        form = FeedbackForm()

    return render(request, 'customertemp/give_feedback.html', {'form': form, 'about_user': about_user,'appointments':appointments})



@login_required(login_url='login_view')
def select_feedback_target(request):
    customer = get_object_or_404(Customers, user=request.user)

    # Get only workers the customer has appointments with
    worker_ids = Appointment.objects.filter(customer=customer).values_list('worker__user__id', flat=True).distinct()
    workers = Worker.objects.filter(user__id__in=worker_ids)

    # Get only nurses the customer has nurse bookings with
    nurse_ids = NurseBooking.objects.filter(customer=customer).values_list('nurse__login__id', flat=True).distinct()
    nurses = Nurse.objects.filter(login__id__in=nurse_ids)

    return render(request, 'customertemp/select_feedback_target.html', {
        'workers': workers,
        'nurses': nurses,
    })

def pay_nurse_booking(request, booking_id):
    booking = get_object_or_404(NurseBooking, id=booking_id, customer__user=request.user)

    # Check if already paid
    if hasattr(booking, 'nursebookingpayment'):
        messages.info(request, "You have already paid for this booking.")
        return redirect('view_my_bookings')

    if request.method == 'POST':
        amount = request.POST.get('amount')  # You can fix amount logic if needed
        if amount:
            NurseBookingPayment.objects.create(
                booking=booking,
                amount=amount,
                payment_status="Paid"
            )
            messages.success(request, "Payment Successful!")
            return redirect('view_my_bookings')
        else:
            messages.error(request, "Invalid amount entered.")

    return render(request, 'customertemp/pay_nurse_booking.html', {'booking': booking})