from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class Login(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)

class Work(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    charge = models.IntegerField()
    Services_image = models.ImageField(upload_to='service')


    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='worker')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=200)
    work_type = models.ForeignKey(Work, on_delete=models.CASCADE)
    id_card = models.ImageField(upload_to='id_cards')
    approval_status = models.BooleanField(default=0)

    def __str__(self):
        return self.name


class Customers(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.name




class CreditCard(models.Model):
    card_no = models.CharField(max_length=30)
    card_cvv = models.CharField(max_length=30)
    expiry_date = models.CharField(max_length=200)


class Schedule(models.Model):
    employee = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Appointment(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='appointment')
    user2 = models.ForeignKey(Worker, on_delete=models.DO_NOTHING)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    Approvel_status = models.BooleanField(default=0)



class Feedback(models.Model):
    user = models.ForeignKey(Login, on_delete=models.DO_NOTHING)
    about_user = models.ForeignKey(Login, on_delete=models.DO_NOTHING, related_name='received_feedbacks')
    subject = models.CharField(max_length=200)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)  # Date auto-set, no manual input needed
    reply = models.TextField(null=True, blank=True)


class Complaints(models.Model):
    user = models.ForeignKey(Login, on_delete=models.DO_NOTHING)
    complaints = models.TextField()
    date = models.DateField()
    reply = models.TextField(null=True, blank=True)
    Complaints_image = models.ImageField(upload_to='Complaints_service', null=True, blank=True)

class Nurse(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    id_card = models.ImageField(upload_to='nurse_idcards/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class NurseBooking(models.Model):
    nurse = models.ForeignKey('Nurse', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    patient_name = models.CharField(max_length=100)
    patient_age = models.IntegerField()
    patient_condition = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # Pending, Accepted, Completed
    created_at = models.DateTimeField(default=timezone.now)



class Appointment(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    amount = models.IntegerField()
    Approvel_status = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()  # product count
    image = models.ImageField(upload_to='product_images/')
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class PaymentToWorker(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Paid")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment from {self.customer.name} to {self.worker.name}"

class Bill(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)  # String reference avoids order issues
    bill_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    paid_on = models.DateField(auto_now=True)
    status = models.IntegerField(default=0)



class NurseBookingPayment(models.Model):
    booking = models.OneToOneField(NurseBooking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, default='Paid')  # Paid, Pending, Failed

    def __str__(self):
        return f"Payment for {self.booking.id} - {self.amount}"