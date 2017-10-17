from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Classes)
admin.site.register(Students)
admin.site.register(Teacher)
admin.site.register(Administrator)