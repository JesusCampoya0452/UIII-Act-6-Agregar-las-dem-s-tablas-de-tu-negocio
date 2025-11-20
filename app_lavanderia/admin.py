from django.contrib import admin
from .models import Servicio, Empleado, Cliente

admin.site.register(Servicio)
admin.site.register(Cliente)
admin.site.register(Empleado)
# Register your models here.
