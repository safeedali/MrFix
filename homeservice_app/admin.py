from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Login)
admin.site.register(models.Worker)
admin.site.register(models.Customers)
admin.site.register(models.Work)
admin.site.register(models.Bill)
admin.site.register(models.Schedule)
admin.site.register(models.Appointment)
admin.site.register(models.Complaints)
