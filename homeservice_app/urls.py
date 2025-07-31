from django.urls import path

from . import views, adminviews, workerviews, customerviews,nurseviews

urlpatterns = [
    path('', views.home_Work, name='home_Work'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('worker_register/', views.worker_register, name='worker_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('nurse_register/', views.nurse_register, name='nurse_register'),
    path('home_Work/', views.home_Work, name='home_Work'),

    path('admin_home/', adminviews.admin_home, name='admin_home'),
    path('view_pending_nurses/', adminviews.view_pending_nurses, name='view_pending_nurses'),
    path('approve_nurse/<int:nurse_id>/', adminviews.approve_nurse, name='approve_nurse'),
    path('reject_nurse/<int:id>/', adminviews.reject_nurse, name='reject_nurse'),
    path('approve_Worker/<int:Worker_id>/', adminviews.approve_Worker, name='approve_Worker'),


    path('workers_view/', adminviews.view_workers, name='workers_view'),
    path('workers_update/<int:id>/', adminviews.workers_update, name='workers_update'),
    path('worker_remove/<int:id>/', adminviews.remove_worker, name='worker_remove'),
    path('customers_view/', adminviews.view_customers, name='customers_view'),
    path('customers_remove/<int:id>/', adminviews.remove_customers, name='customers_remove'),
    path('work_add/', adminviews.add_work, name='work_add'),
    path('work_view/', adminviews.view_work, name='work_view'),
    path('work_update/<int:id>/', adminviews.update_work, name='work_update'),
    path('work_delete/<int:id>/', adminviews.delete_work, name='work_delete'),
    path('appointment_admin', adminviews.appointment_admin, name='appointment_admin'),
    path('approve_appointment/<int:id>/', adminviews.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:id>/', adminviews.reject_appointment, name='reject_appointment'),
    path('Feedback_admin/', adminviews.Feedback_admin, name='Feedback_admin'),
    path('reply_Feedback/<int:id>/', adminviews.reply_Feedback, name='reply_Feedback'),
    path('add_bill/', adminviews.bill, name='add_bill'),
    path('view_bill/', adminviews.view_bill, name='view_bill'),

    path('view_complaints/', adminviews.view_complaints, name='view_complaints'),
    path('reply_complaint/<int:complaint_id>/', adminviews.reply_complaint, name='reply_complaint'),
    path('view_all_nurse_bookings', adminviews.view_all_nurse_bookings, name='view_all_nurse_bookings'),
    path('Nurseapprove_booking/<int:booking_id>/', adminviews.Nurseapprove_booking, name='Nurseapprove_booking'),
    path('reject_booking/<int:booking_id>/', adminviews.reject_booking, name='reject_booking'),
    path('Verified_Worker_view', adminviews.Verified_Worker_view, name='Verified_Worker_view'),
    path('Verified_Nurse_view', adminviews.Verified_Nurse_view, name='Verified_Nurse_view'),
    path('add_product', adminviews.add_product, name='add_product'),
    path('view_product', adminviews.view_product, name='view_product'),
    path('adminpanel/bookings/', adminviews.admin_booking_list, name='admin_booking_list'),
    path('adminpanel/approve_booking/<int:appointment_id>/', adminviews.approve_booking, name='approve_booking'),
    path('adminpanel/delete_booking/<int:appointment_id>/', adminviews.delete_booking, name='delete_booking'),
    path('approve_booking/<int:booking_id>/', adminviews.approve_booking, name='approve_booking'),
    path('view_Customers_Booking', adminviews.view_Customers_Booking, name='view_Customers_Booking'),
    path('pay_to_worker/<int:appointment_id>/', adminviews.pay_to_worker, name='pay_to_worker'),
    path('products/', adminviews.view_product, name='view_product'),
    path('products/update/<int:pk>/', adminviews.update_product, name='update_product'),


    path('worker_home/', workerviews.worker_home, name='worker_home'),
    path('schedule_add/', workerviews.schedule_add, name='schedule_add'),
    path('schedule_view', workerviews.schedule_view, name='schedule_view'),
    path('schedule_update/<int:id>/', workerviews.schedule_update, name='schedule_update'),
    path('schedule_delete/<int:id>/', workerviews.schedule_delete, name='schedule_delete'),
    path('view_payment_details_worker/', workerviews.view_payment_details_worker, name='view_payment_details_worker'),
    path('appointment_view_worker/', workerviews.appointment_view_worker, name='appointment_view_worker'),
    path('worker_feedback_view/', workerviews.worker_feedback_view, name='worker_feedback_view'),
    path('schedule_view/', workerviews.schedule_view, name='schedule_view'),
    path('Worker_appointment_view/', workerviews.Worker_appointment_view, name='Worker_appointment_view'),
    path('Worker_appointment_view/', workerviews.Worker_appointment_view, name='Worker_appointment_view'),
    path('Worker_appointment_view/', workerviews.Worker_appointment_view, name='Worker_appointment_view'),

    path('customer_home/', customerviews.customer_home, name='customer_home'),
    path('view_workers/', customerviews.view_workers_customer, name='view_workers'),
    path('view_schedule/<int:work_id>/', customerviews.view_schedule_customer, name='view_schedule_customer'),
    # path('take_appointment/<int:id>/', customerviews.take_appointment, name='take_appointment'),
    path('Myappointment_view', customerviews.Myappointment_view, name='Myappointment_view'),
    path('give_feedback/<int:about_user_id>/', customerviews.give_feedback, name='give_feedback'),
    path('Feedback_view_user', customerviews.Feedback_view_user, name='Feedback_view_user'),
    path('view_bill_user', customerviews.view_bill_user, name='view_bill_user'),
    path('pay_bill/<int:bill_id>/', customerviews.pay_bill, name='pay_bill'),
    path('pay_in_direct/<int:id>/', customerviews.pay_in_direct, name='pay_in_direct'),
    path('bill_history', customerviews.bill_history, name='bill_history'),
    path('Complaints_add_user', customerviews.Complaints_add_user, name='Complaints_add_user'),
    path('prod_cus', customerviews.prod_cus, name='prod_cus'),
    path('book_schedule/<int:schedule_id>/', customerviews.book_schedule, name='book_schedule'),
    path('make_payment/<int:appointment_id>/', customerviews.make_payment, name='make_payment'),
    path('select_feedback_target/', customerviews.select_feedback_target, name='select_feedback_target'),
    path('pay_nurse_booking/<int:booking_id>/', customerviews.pay_nurse_booking, name='pay_nurse_booking'),

    path('complaint_reply_view', customerviews.complaint_reply_view, name='complaint_reply_view'),
    path('book_appointment/<int:schedule_id>/', customerviews.book_appointment, name='book_appointment'),
    path('approve_WorkK/<int:id>/', customerviews.approve_WorkK, name='approve_WorkK'),

    path('View_Services', customerviews.View_Services, name='View_Services'),
    path('view_nurses', customerviews.view_nurses, name='view_nurses'),
    path('book_nurse/<int:nurse_id>', customerviews.book_nurse, name='book_nurse'),
    path('view_my_bookings', customerviews.view_my_bookings, name='view_my_bookings'),


    path('nurseHome', nurseviews.nurseHome, name='nurseHome'),
    path('nurse_appointment_view', nurseviews.nurse_appointment_view, name='nurse_appointment_view'),
    path('view_my_feedback_nurse/', nurseviews.view_my_feedback_nurse, name='view_my_feedback_nurse'),
    path('nurse_view_payments/', nurseviews.nurse_view_payments, name='nurse_view_payments'),






]
