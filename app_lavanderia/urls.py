# app_lavanderia/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rutas para la página de inicio
    path('', views.inicio_lavanderia, name='inicio_lavanderia'),

    # Rutas para el modelo Cliente
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:id>/', views.borrar_cliente, name='borrar_cliente'),

    # Rutas para el modelo Empleado <--- ¡Asegúrate de que estas existan!
    path('empleados/', views.ver_empleados, name='ver_empleados'), # <--- ESTA ES LA CLAVE
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),

        # Rutas para el modelo Empleado <--- ¡Asegúrate de que estas existan!
    path('servicios/', views.ver_servicios, name='ver_servicios'), # <--- ESTA ES LA CLAVE
    path('servicios/agregar/', views.agregar_servicio, name='agregar_servicio'),
    path('servicios/actualizar/<int:id>/', views.actualizar_servicio, name='actualizar_servicio'),
    path('servicios/borrar/<int:id>/', views.borrar_servicio, name='borrar_servicio'),

    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:id_prove>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/borrar/<int:id_prove>/', views.borrar_proveedor, name='borrar_proveedor'),

    # Rutas para el modelo Producto
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:id_prd>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/borrar/<int:id_prd>/', views.borrar_producto, name='borrar_producto'),

    # Rutas para el modelo Pedido
    path('pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedidos/actualizar/<int:id_pedido>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedidos/borrar/<int:id_pedido>/', views.borrar_pedido, name='borrar_pedido'),
]