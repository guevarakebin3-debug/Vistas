from django.contrib import admin
from .models import Cargo, Empleado


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'correo', 'sueldo', 'fecha_ingreso', 'cargo')
    list_filter = ('cargo',)
    search_fields = ('nombres', 'apellidos', 'correo')
