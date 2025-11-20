from django.db import models

# ==========================================
# MODELO: CLIENTE
# ==========================================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: EMPLEADO
# ==========================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=8, decimal_places=2)
    # La relación ManyToMany se define aquí.
    # Un Empleado puede estar asignado a muchos Servicios.
    # Un Servicio puede tener muchos Empleados asignados.
    servicios = models.ManyToManyField('Servicio', related_name='empleados')


    def __str__(self):
        return f"{self.nombre} ({self.puesto})"


# ==========================================
# MODELO: SERVICIO
# ==========================================
class Servicio(models.Model):
    # Relación uno a muchos: Un Servicio pertenece a un Cliente.
    # Un Cliente puede tener muchos Servicios.
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='servicios')

    tipo_servicio = models.CharField(max_length=100)
    fecha_servicio = models.DateField()
    hora_entrega = models.TimeField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En proceso', 'En proceso'),
            ('Completado', 'Completado')
        ],
        default='Pendiente'
    )
    forma_pago = models.CharField(max_length=50, default='Efectivo')

    def __str__(self):
        return f"{self.tipo_servicio} - {self.cliente.nombre}"

# ... (Modelos Cliente y Empleado igual que antes) ...

# ==========================================
# MODELO: SERVICIO
# ==========================================

def __str__(self):
    return f"Pedido #{self.id_pedido} - {self.estado}"

# Puedes añadir un método para calcular el total si lo deseas
def calcular_total(self):
    # Esto es un ejemplo, necesitarías una tabla intermedia para guardar la cantidad de cada producto
    # por ahora, solo sumaremos los precios de los productos si no tienes la cantidad.
    # Para un total preciso, se usaría un modelo intermedio con 'through'
    total_calculado = sum(producto.precio for producto in self.productos.all())
    self.total = total_calculado
    self.save() # Guarda el total calculado en la base de datos

class Meta:
    verbose_name = "Pedido"
    verbose_name_plural = "Pedidos"
    # db_table = 'pedidos'

# ==========================================
# MODELO: PROVEEDOR (CORREGIDO)
# ==========================================
# Nota: He movido esta clase hacia atrás (sin sangría) para que sea un modelo independiente.
class Proveedor(models.Model):
    id_prove = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    domicilio = models.CharField(max_length=200, blank=True, null=True)
    producto_principal = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_principales')

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: PRODUCTO
# ==========================================
class Producto(models.Model):
    id_prd = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50) 
    fecha_vencimiento = models.DateField(blank=True, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_llegada = models.DateField(auto_now_add=True) 

    # AHORA SI FUNCIONARÁ LA LÍNEA 97
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='productos_suministrados')

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True) # id_pedido será el campo de ID principal y autoincremental
    fecha = models.DateField(auto_now_add=True) # Fecha de creación del pedido
    estado_choices = [
    ('Pendiente', 'Pendiente'),
    ('En Proceso', 'En Proceso'),
    ('Completado', 'Completado'),
    ('Cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=estado_choices, default='Pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_entrega = models.DateField(blank=True, null=True) # Fecha estimada o real de entrega
    # Relación de Muchos a Muchos con Producto (id_prd en tu descripción, aquí es 'productos')
    # Un pedido puede tener MUCHOS productos, y un producto puede estar en MUCHOS pedidos.
    productos = models.ManyToManyField(Producto, related_name='pedidos')
    # Django creará automáticamente una tabla intermedia para manejar esta relación.

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.estado}"

    # Puedes añadir un método para calcular el total si lo deseas
    def calcular_total(self):
        # Esto es un ejemplo, necesitarías una tabla intermedia para guardar la cantidad de cada producto
        # por ahora, solo sumaremos los precios de los productos si no tienes la cantidad.
        # Para un total preciso, se usaría un modelo intermedio con 'through'
        total_calculado = sum(producto.precio for producto in self.productos.all())
        self.total = total_calculado
        self.save() # Guarda el total calculado en la base de datos

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        # db_table = 'pedidos'

    # ... (Modelo Pedido igual que antes) ...