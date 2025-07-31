from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


from .forms import Workform, LoginRegister, WorkerRegister, AddBill,NurseBooking,ProductForm
from .models import Worker, Login, Customers, Work, Appointment, Feedback, Bill, Complaints, Nurse, Product


@login_required(login_url='login_view')
def admin_home(request):
    total_workers = Worker.objects.count()
    total_customers = Customers.objects.count()
    total_appointments = Appointment.objects.count()

    return render(request, 'admintemp/admin_home.html',{'total_workers':total_workers,'total_customers':total_customers,'total_appointments':total_appointments})


@login_required(login_url='login_view')
def view_workers(request):
    data = Worker.objects.all()
    return render(request, 'admintemp/workers.html', {'data': data})


@login_required(login_url='login_view')
def workers_update(request, id):
    w = Worker.objects.get(id=id)
    # l = Login.objects.get(worker=w)
    if request.method == 'POST':
        form = WorkerRegister(request.POST or None, instance=w)
        # user_form = LoginRegister(request.POST or None, instance=l)
        if form.is_valid():
            form.save()
            # user_form.save()
            messages.info(request, 'workers updated successful')
            return redirect('workers_view')
    else:
        form = WorkerRegister(instance=w)
        # user_form = LoginRegister(instance=l)
    return render(request, 'admintemp/worker_update.html', {'form': form})


@login_required(login_url='login_view')
def remove_worker(request, id):
    data1 = Worker.objects.get(id=id)
    data = Login.objects.get(worker=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('workers_view')
    else:
        return redirect('workers_view')


@login_required(login_url='login_view')
def view_customers(request):
    data = Customers.objects.all()
    return render(request, 'admintemp/customers.html', {'data': data})


@login_required(login_url='login_view')
def remove_customers(request, id):
    data1 = Customers.objects.get(id=id)
    data = Login.objects.get(customer=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('customers_view')
    else:
        return redirect('customers_view')


@login_required(login_url='login_view')
def add_work(request):
    if request.method == 'POST':
        form = Workform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('work_view')
    else:
        form = Workform()
    return render(request, 'admintemp/work_add.html', {'form': form})


@login_required(login_url='login_view')
def view_work(request):
    data = Work.objects.all()
    return render(request, 'admintemp/work.html', {'data': data})


@login_required(login_url='login_view')
def update_work(request, id):
    data = Work.objects.get(id=id)
    if request.method == 'POST':
        form = Workform(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            return redirect('work_view')
    else:
        form = Workform(request.POST or None, instance=data)
    return render(request, 'admintemp/work_update.html', {'form': form})


@login_required(login_url='login_view')
def delete_work(request, id):
    data = Work.objects.get(id=id)
    data.delete()
    return redirect('work_view')


@login_required(login_url='login_view')
def appointment_admin(request):
    a = Appointment.objects.all()
    context = {
        'appointment': a,
    }
    return render(request, 'admintemp/appointments.html', context)


@login_required(login_url='login_view')
def approve_appointment(request, id):
    a = Appointment.objects.get(id=id)
    a.status = 1
    a.save()
    messages.info(request, 'Appointment  Confirmed')
    return redirect('appointment_admin')


@login_required(login_url='login_view')
def reject_appointment(request, id):
    n = Appointment.objects.get(id=id)
    n.status = 2
    n.save()
    messages.info(request, 'Appointment Rejected')
    return redirect('appointment_admin')


@login_required(login_url='login_view')
def Feedback_admin(request):
    f = Feedback.objects.all()
    return render(request, 'admintemp/complaint_view.html', {'feedback': f})


@login_required(login_url='login_view')
def reply_Feedback(request, id):
    f = Feedback.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('Feedback_admin')
    return render(request, 'admintemp/reply_complaint.html', {'feedback': f})


def bill(request):
    form = AddBill()
    if request.method == 'POST':
        form = AddBill(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_bill')
    return render(request, 'admintemp/generate_bill.html', {'form': form})


def view_bill(request):
    bill = Bill.objects.all()
    print(bill)
    return render(request, 'admintemp/view_payment_details.html', {'bills': bill})


def view_complaints(request):
    complaints = Complaints.objects.all()
    return render(request, 'admintemp/view_complaints.html', {'complaints': complaints})



def reply_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaints, id=complaint_id)
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        complaint.reply = reply_text
        complaint.save()
        return redirect('view_complaints')
    return render(request, 'admintemp/reply_Priver_complaint.html', {'complaint': complaint})



def view_pending_nurses(request):
    nurses = Nurse.objects.filter(approved=False)
    return render(request, 'admintemp/view_pending_nurses.html', {'nurses': nurses})



def approve_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    nurse.approved = True
    nurse.save()
    return redirect('view_pending_nurses')




def reject_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)

    # Also delete the associated login if needed
    if nurse.login:
        nurse.login.delete()  # Deletes both login and cascades if Nurse is OneToOne
    else:
        nurse.delete()

    return redirect('view_pending_nurses')


def view_all_nurse_bookings(request):
    bookings = NurseBooking.objects.all().order_by('-created_at')
    return render(request, 'admintemp/view_all_nurse_bookings.html', {'bookings': bookings})


def Nurseapprove_booking(request, booking_id):
    booking = get_object_or_404(NurseBooking, id=booking_id)
    booking.status = 'Accepted'
    booking.save()
    return redirect('view_all_nurse_bookings')

def reject_booking(request, booking_id):
    booking = get_object_or_404(NurseBooking, id=booking_id)
    booking.status = 'Rejected'
    booking.save()
    return redirect('view_all_nurse_bookings')


def Verified_Worker_view(request):
    data =Worker.objects.all()
    return render(request,'admintemp/Verified_Worker_view.html',{'data':data})


def Verified_Nurse_view(request):
    data = Nurse.objects.filter(approved=True)
    return render(request,'admintemp/Verified_Nurse_view.html',{'data':data})


def add_product(request):
    if not request.user.is_superuser:  # Ensure only admin can access
        messages.error(request, "Permission Denied.")
        return redirect('home')  # Redirect unauthorized users

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('view_product')  # Redirect to product list
        else:
            messages.error(request, "There was an error adding the product. Please check the form.")
    else:
        form = ProductForm()

    return render(request, 'admintemp/add_product.html', {'form': form})




def view_product(request):
    products = Product.objects.all()
    return render(request, 'admintemp/Prod_view.html', {'products': products})


def approve_Worker(request, Worker_id):
    worker = Worker.objects.get(id=Worker_id)
    worker.approval_status = 1
    worker.save()
    return redirect('workers_view')


def approve_Work(request, id):
    work = Appointment.objects.get(id=id)
    work.approval_status = 1
    work.save()
    return redirect('workers_view')

# Function to check if user is admin (adjust logic if needed)
def is_admin(user):
    return user.is_staff  # Or use a custom flag if you have one

@login_required
@user_passes_test(is_admin)
def admin_booking_list(request):
    bookings = Appointment.objects.select_related('customer', 'worker', 'schedule').all()
    return render(request, 'admintemp/booking_list.html', {'bookings': bookings})

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if not appointment.Approvel_status:
        appointment.Approvel_status = True
        appointment.save()

        # Create Bill only if it doesn't exist for this appointment
        existing_bill = Bill.objects.filter(name=appointment.customer, amount=appointment.amount, status=0).first()

        if not existing_bill:
            Bill.objects.create(
                name=appointment.customer,
                amount=appointment.amount,
                status=0  # 0 = Unpaid
            )

    return redirect('admin_booking_list')

@login_required
@user_passes_test(is_admin)
def delete_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('admin_booking_list')

# ______________________________________Updated Code__________________________________________________________________________________________

def view_Customers_Booking(request):
    Customers_Booking = Appointment.objects.all()
    return render(request, 'admintemp/View_Cus_Booking.html', {'Customers_Booking': Customers_Booking})


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def approve_booking(request, booking_id):
    booking = get_object_or_404(Appointment, id=booking_id)
    booking.Approvel_status = True
    booking.status = "Approved"
    booking.save()
    messages.success(request, "Booking Approved Successfully")
    return redirect('view_Customers_Booking')

@staff_member_required(login_url='admin_login')
def pay_to_worker(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Allow only if status is Confirmed
    if appointment.status == 'Confirmed':
        appointment.status = 'Completed'
        appointment.save()

    return redirect('view_Customers_Booking')  # Redirect to your admin booking page


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_product')  # Redirect to the product listing
    else:
        form = ProductForm(instance=product)
    return render(request, 'admintemp/update_product.html', {'form': form, 'product': product})