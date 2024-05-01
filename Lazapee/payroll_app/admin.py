from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Account)

#For Project
admin.site.register(Employee)
admin.site.register(PaySlip)