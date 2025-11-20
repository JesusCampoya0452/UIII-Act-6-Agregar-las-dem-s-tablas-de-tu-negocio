from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Empleado, Servicio, Proveedor, Producto, Pedido # Importa los nuevos modelos
from datetime import datetime

# ==========================================
# VISTA: PÁGINA DE INICIO
# ==========================================
def inicio_lavanderia(request):
    """
    Renderiza la página de inicio de la aplicación de lavandería.
    """
    return render(request, 'inicio.html')

# ==========================================
# VISTAS CRUD PARA EL MODELO CLIENTE
# ==========================================

def agregar_cliente(request):
    """
    Maneja la adición de un nuevo cliente.
    Si la solicitud es POST, procesa los datos del formulario y guarda el cliente.
    Si la solicitud es GET, renderiza el formulario para agregar cliente.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST['direccion']
        notas = request.POST.get('notas', '') # 'notas' puede ser opcional

        nuevo_cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            notas=notas
        )
        nuevo_cliente.save()
        return redirect('ver_clientes') # Redirige a la lista de clientes
    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    """
    Muestra una lista de todos los clientes existentes.
    """
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, id):
    """
    Maneja la actualización de un cliente existente.
    Si la solicitud es POST, procesa los datos del formulario y actualiza el cliente.
    Si la solicitud es GET, renderiza el formulario pre-llenado para actualizar cliente.
    """
    cliente = get_object_or_404(Cliente, id=id) # Obtiene el cliente o devuelve 404
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.telefono = request.POST['telefono']
        cliente.correo = request.POST['correo']
        cliente.direccion = request.POST['direccion']
        cliente.notas = request.POST.get('notas', '')
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def borrar_cliente(request, id):
    """
    Elimina un cliente específico de la base de datos.
    """
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('ver_clientes')

# ==========================================
# VISTAS CRUD PARA EL MODELO EMPLEADO
# ==========================================

def agregar_empleado(request):
    """
    Maneja la adición de un nuevo empleado.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        puesto = request.POST['puesto']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        fecha_contratacion = request.POST['fecha_contratacion'] # Formato 'YYYY-MM-DD'
        salario = request.POST['salario']

        nuevo_empleado = Empleado(
            nombre=nombre,
            apellido=apellido,
            puesto=puesto,
            telefono=telefono,
            correo=correo,
            fecha_contratacion=fecha_contratacion,
            salario=salario
        )
        nuevo_empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/agregar_empleado.html')

def ver_empleados(request):
    """
    Muestra una lista de todos los empleados existentes.
    """
    empleados = Empleado.objects.all()
    return render(request, 'empleado/ver_empleados.html', {'empleados': empleados})

def actualizar_empleado(request, id):
    """
    Maneja la actualización de un empleado existente.
    """
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.puesto = request.POST['puesto']
        empleado.telefono = request.POST['telefono']
        empleado.correo = request.POST['correo']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado})

def borrar_empleado(request, id):
    """
    Elimina un empleado específico de la base de datos.
    """
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    return redirect('ver_empleados')

# ==========================================
# VISTAS CRUD PARA EL MODELO SERVICIO
# ==========================================

def agregar_servicio(request):
    """
    Maneja la adición de un nuevo servicio. Requiere seleccionar un cliente
    y puede asignar múltiples empleados.
    """
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        empleados_ids = request.POST.getlist('empleados') # getlist para múltiples selecciones
        tipo_servicio = request.POST['tipo_servicio']
        fecha_servicio = request.POST['fecha_servicio'] # Formato 'YYYY-MM-DD'
        hora_entrega = request.POST['hora_entrega']     # Formato 'HH:MM'
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        estado = request.POST['estado']
        forma_pago = request.POST['forma_pago']

        cliente = get_object_or_404(Cliente, id=cliente_id)

        nuevo_servicio = Servicio(
            cliente=cliente,
            tipo_servicio=tipo_servicio,
            fecha_servicio=fecha_servicio,
            hora_entrega=hora_entrega,
            descripcion=descripcion,
            precio=precio,
            estado=estado,
            forma_pago=forma_pago
        )
        nuevo_servicio.save()
        # Asigna los empleados después de guardar el servicio para que tenga un ID
        if empleados_ids:
            nuevo_servicio.empleados.set(empleados_ids)
        return redirect('ver_servicios')
    return render(request, 'servicio/agregar_servicio.html', {'clientes': clientes, 'empleados': empleados})

def ver_servicios(request):
    """
    Muestra una lista de todos los servicios existentes.
    """
    servicios = Servicio.objects.all().select_related('cliente').prefetch_related('empleados')
    return render(request, 'servicio/ver_servicios.html', {'servicios': servicios})

def actualizar_servicio(request, id):
    """
    Maneja la actualización de un servicio existente.
    """
    servicio = get_object_or_404(Servicio, id=id)
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    
    if request.method == 'POST':
        servicio.cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        servicio.tipo_servicio = request.POST['tipo_servicio']
        servicio.fecha_servicio = request.POST['fecha_servicio']
        servicio.hora_entrega = request.POST['hora_entrega']
        servicio.descripcion = request.POST['descripcion']
        servicio.precio = request.POST['precio']
        servicio.estado = request.POST['estado']
        servicio.forma_pago = request.POST['forma_pago']
        servicio.save()
        
        empleados_ids = request.POST.getlist('empleados')
        servicio.empleados.set(empleados_ids) # Actualiza la relación ManyToMany
        
        return redirect('ver_servicios')
    
    # Preseleccionar empleados actuales para el formulario
    empleados_seleccionados = servicio.empleados.all()
    return render(request, 'servicio/actualizar_servicio.html', {
        'servicio': servicio,
        'clientes': clientes,
        'empleados': empleados,
        'empleados_seleccionados': empleados_seleccionados,
    })

def borrar_servicio(request, id):
    """
    Elimina un servicio específico de la base de datos.
    """
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('ver_servicios')


# ==========================================
# VISTAS CRUD PARA EL MODELO PROVEEDOR
# ==========================================

def agregar_proveedor(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST.get('telefono')
        domicilio = request.POST.get('domicilio')
        producto_principal_id = request.POST.get('id_prd2')

        nuevo_proveedor = Proveedor(nombre=nombre, telefono=telefono, domicilio=domicilio)
        if producto_principal_id:
            producto_principal = get_object_or_404(Producto, id_prd=producto_principal_id)
            nuevo_proveedor.producto_principal = producto_principal
        nuevo_proveedor.save()
        return redirect('ver_proveedores')
    return render(request, 'proveedor/agregar_proveedor.html', {'productos': productos})

def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/ver_proveedores.html', {'proveedores': proveedores})

def actualizar_proveedor(request, id_prove):
    proveedor = get_object_or_404(Proveedor, id_prove=id_prove)
    productos = Producto.objects.all()
    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.telefono = request.POST.get('telefono')
        proveedor.domicilio = request.POST.get('domicilio')
        producto_principal_id = request.POST.get('id_prd2')
        if producto_principal_id:
            producto_principal = get_object_or_404(Producto, id_prd=producto_principal_id)
            proveedor.producto_principal = producto_principal
        else:
            proveedor.producto_principal = None
        proveedor.save()
        return redirect('ver_proveedores')
    return render(request, 'proveedor/actualizar_proveedor.html', {'proveedor': proveedor, 'productos': productos})

def borrar_proveedor(request, id_prove):
    proveedor = get_object_or_404(Proveedor, id_prove=id_prove)
    proveedor.delete()
    return redirect('ver_proveedores')


# ==========================================
# VISTAS CRUD PARA EL MODELO PRODUCTO
# ==========================================

def agregar_producto(request):
    proveedores = Proveedor.objects.all() # Necesitamos los proveedores para el select
    if request.method == 'POST':
        nombre = request.POST['nombre']
        unidad_medida = request.POST['unidad_medida']
        fecha_vencimiento_str = request.POST.get('fecha_vencimiento')
        precio = request.POST['precio']
        proveedor_id = request.POST.get('proveedor') # Puede ser None si no se selecciona

        fecha_vencimiento = None
        if fecha_vencimiento_str:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d').date()

        producto_proveedor = None
        if proveedor_id:
            producto_proveedor = get_object_or_404(Proveedor, id_prove=proveedor_id)

        nuevo_producto = Producto(
            nombre=nombre,
            unidad_medida=unidad_medida,
            fecha_vencimiento=fecha_vencimiento,
            precio=precio,
            proveedor=producto_proveedor
        )
        nuevo_producto.save()
        return redirect('ver_productos')
    return render(request, 'producto/agregar_producto.html', {'proveedores': proveedores})

def ver_productos(request):
    productos = Producto.objects.all().select_related('proveedor') # Para cargar el proveedor en una sola consulta
    return render(request, 'producto/ver_productos.html', {'productos': productos})

def actualizar_producto(request, id_prd):
    producto = get_object_or_404(Producto, id_prd=id_prd)
    proveedores = Proveedor.objects.all() # Necesitamos los proveedores para el select
    
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.unidad_medida = request.POST['unidad_medida']
        
        fecha_vencimiento_str = request.POST.get('fecha_vencimiento')
        producto.fecha_vencimiento = None
        if fecha_vencimiento_str:
            producto.fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d').date()

        producto.precio = request.POST['precio']
        
        proveedor_id = request.POST.get('proveedor')
        producto.proveedor = None
        if proveedor_id:
            producto.proveedor = get_object_or_404(Proveedor, id_prove=proveedor_id)
        
        producto.save()
        return redirect('ver_productos')
    return render(request, 'producto/actualizar_producto.html', {'producto': producto, 'proveedores': proveedores})

def borrar_producto(request, id_prd):
    producto = get_object_or_404(Producto, id_prd=id_prd)
    producto.delete()
    return redirect('ver_productos')


# ==========================================
# VISTAS CRUD PARA EL MODELO PEDIDO
# ==========================================

def agregar_pedido(request):
    productos = Producto.objects.all() # Necesitamos los productos para el selector de muchos a muchos
    if request.method == 'POST':
        estado = request.POST['estado']
        fecha_entrega_str = request.POST.get('fecha_entrega')
        productos_ids = request.POST.getlist('productos') # Obtener la lista de IDs de productos seleccionados

        fecha_entrega = None
        if fecha_entrega_str:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()

        nuevo_pedido = Pedido(
            estado=estado,
            fecha_entrega=fecha_entrega
        )
        nuevo_pedido.save() # Guardar primero el pedido para poder asignar productos (relación M2M)

        if productos_ids:
            nuevo_pedido.productos.set(productos_ids) # Asignar los productos al pedido
        
        # Calcular y guardar el total después de asignar los productos
        nuevo_pedido.calcular_total() 
        
        return redirect('ver_pedidos')
    return render(request, 'pedido/agregar_pedido.html', {'productos': productos})


def ver_pedidos(request):
    # Usamos prefetch_related para cargar los productos relacionados de cada pedido en una sola consulta
    pedidos = Pedido.objects.all().prefetch_related('productos')
    return render(request, 'pedido/ver_pedidos.html', {'pedidos': pedidos})

def actualizar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    productos = Producto.objects.all() # Necesitamos todos los productos para el selector

    if request.method == 'POST':
        pedido.estado = request.POST['estado']
        
        fecha_entrega_str = request.POST.get('fecha_entrega')
        pedido.fecha_entrega = None
        if fecha_entrega_str:
            pedido.fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
        
        pedido.save() # Guardar los campos directos

        productos_ids = [id for id in request.POST.getlist('productos') if id]
        pedido.productos.set(productos_ids)

        # Recalcular el total después de actualizar los productos
        pedido.calcular_total()

        return redirect('ver_pedidos')
    
    # Obtener los IDs de productos actualmente seleccionados para preseleccionar en el formulario
    productos_seleccionados_ids = [p.id_prd for p in pedido.productos.all()]

    return render(request, 'pedido/actualizar_pedido.html', {
        'pedido': pedido,
        'productos': productos,
        'productos_seleccionados_ids': productos_seleccionados_ids
    })

def borrar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedido.delete()
    return redirect('ver_pedidos')