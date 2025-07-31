import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


from . models import Login, Worker, Customers, Work, Schedule, CreditCard, Feedback, Bill,Complaints,Nurse,NurseBooking,Product


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')


class LoginRegister(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(LoginRegister, self).__init__(*args, **kwargs)

        # Remove help texts
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        for field in self.fields.values():
            field.label_suffix = ""


class WorkerRegister(forms.ModelForm):
    contact_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Worker
        fields = ('name', 'contact_no', 'email', 'address', 'work_type', 'id_card')


class CustomerRegister(forms.ModelForm):
    contact_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Customers
        fields = ('name', 'contact_no', 'email', 'address')


class Workform(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'


class SchdeuleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput, )
    end_time = forms.TimeField(widget=TimeInput, )

    class Meta:
        model = Schedule
        fields = ('date', 'start_time', 'end_time')


class AddBill(forms.ModelForm):
    # name = forms.ModelChoiceField(queryset=Customers.objects.filter(role='customer'))

    class Meta:
        model = Bill
        exclude = ('status', 'paid_on')


class PayBillForm(forms.ModelForm):
    card_no = forms.CharField(validators=[RegexValidator(regex='^.{16}$', message='Please Enter a Valid Card No')])
    card_cvv = forms.CharField(widget=forms.PasswordInput,
                               validators=[RegexValidator(regex='^.{3}$', message='Please Enter a Valid CVV')])
    expiry_date = forms.DateField(widget=DateInput(attrs={'id': 'example-month-input'}))

    class Meta:
        model = CreditCard
        fields = ('card_no', 'card_cvv', 'expiry_date')





class ComplaintsForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = Complaints
        fields = ('complaints', 'date','Complaints_image')

class NurseRegisterForm(forms.ModelForm):
    contact_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Nurse
        fields = ('name', 'contact_no', 'email', 'address', 'qualification', 'experience', 'id_card')


class NurseBookingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput)
    end_time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = NurseBooking
        fields = ['date', 'start_time', 'end_time', 'patient_name', 'patient_age', 'patient_condition']







from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'




class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'feedback']  # Only include editable fields
