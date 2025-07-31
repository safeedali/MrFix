from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Nurse, Work
# Create your views here.
from .forms import LoginRegister, WorkerRegister, CustomerRegister,NurseRegisterForm


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_nurse:
                nurse = Nurse.objects.get(login=user)
                if not nurse.approved:
                    messages.info(request, "Your account is pending admin approval.")
                    return render(request, 'login.html')
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user is not None and user.is_worker:
                if user.worker.approval_status == True:
                    return redirect('worker_home')
            elif user.is_customer:
                return redirect('customer_home')
            elif user.is_nurse:
                return redirect('nurseHome')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'login.html')


def worker_register(request):
    user_form = LoginRegister()
    worker_form = WorkerRegister()
    if request.method == 'POST':
        user_form = LoginRegister(request.POST)
        worker_form = WorkerRegister(request.POST, request.FILES)
        if user_form.is_valid() and worker_form.is_valid():
            user = user_form.save(commit=False)
            user.is_worker = True
            user.save()
            worker = worker_form.save(commit=False)
            worker.user = user
            worker.save()
            messages.info(request, 'Registered Successfully')
            return redirect('login')
    return render(request, 'worker_register.html', {'user_form': user_form, 'worker_form': worker_form})


def customer_register(request):
    user_form = LoginRegister()
    customer_form = CustomerRegister()
    if request.method == 'POST':
        user_form = LoginRegister(request.POST)
        customer_form = CustomerRegister(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.is_customer = True
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            messages.info(request, 'Registered Successfully')
            return redirect('login')
    return render(request, 'customer_register.html', {'user_form': user_form, 'customer_form': customer_form})



def nurse_register(request):
    if request.method == 'POST':
        user_form = LoginRegister(request.POST)
        nurse_form = NurseRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and nurse_form.is_valid():
            user = user_form.save(commit=False)
            user.is_nurse = True
            user.save()
            nurse = nurse_form.save(commit=False)
            nurse.login = user
            nurse.approved = False
            nurse.save()
            return redirect('login')
    else:
        user_form = LoginRegister()
        nurse_form = NurseRegisterForm()
    return render(request, 'nursetemp/nurse_register.html', {'user_form': user_form, 'nurse_form': nurse_form})





def logout_view(request):
    logout(request)
    return redirect('login')


def sample_test(request):
    return render(request, 'customer_register.html')

def home_Work(request):
    works = Work.objects.all()
    return render(request,'home.html',{'works':works})