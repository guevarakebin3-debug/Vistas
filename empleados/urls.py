from django.urls import path
from . import views

urlpatterns = [
    # ---------- VBF: Vistas Basadas en Funciones ----------
    path('fbv/cargos/', views.cargo_list, name='fbv_cargo_list'),
    path('fbv/cargos/crear/', views.cargo_create, name='fbv_cargo_create'),
    path('fbv/cargos/<int:pk>/editar/', views.cargo_update, name='fbv_cargo_update'),
    path('fbv/cargos/<int:pk>/eliminar/', views.cargo_delete, name='fbv_cargo_delete'),

    path('fbv/empleados/', views.empleado_list, name='fbv_empleado_list'),
    path('fbv/empleados/crear/', views.empleado_create, name='fbv_empleado_create'),
    path('fbv/empleados/<int:pk>/editar/', views.empleado_update, name='fbv_empleado_update'),
    path('fbv/empleados/<int:pk>/eliminar/', views.empleado_delete, name='fbv_empleado_delete'),

    # ---------- VBC: Vistas Basadas en Clases ----------
    path('cbv/cargos/', views.CargoListView.as_view(), name='cbv_cargo_list'),
    path('cbv/cargos/crear/', views.CargoCreateView.as_view(), name='cbv_cargo_create'),
    path('cbv/cargos/<int:pk>/editar/', views.CargoUpdateView.as_view(), name='cbv_cargo_update'),
    path('cbv/cargos/<int:pk>/eliminar/', views.CargoDeleteView.as_view(), name='cbv_cargo_delete'),

    path('cbv/empleados/', views.EmpleadoListView.as_view(), name='cbv_empleado_list'),
    path('cbv/empleados/crear/', views.EmpleadoCreateView.as_view(), name='cbv_empleado_create'),
    path('cbv/empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='cbv_empleado_update'),
    path('cbv/empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='cbv_empleado_delete'),
]
