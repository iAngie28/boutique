from django.db import models

# Create your models here.
# boutique/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone


# =========================
#  Gestión de usuarios
# =========================

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.TextField(blank=True, help_text="Descripción/JSON de permisos (opcional)")

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    roles = models.ManyToManyField(Rol, blank=True, related_name="usuarios")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()


class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="administrador")

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"Administrador: {self.usuario}"


class Cajero(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="cajero")
    horario = models.CharField(max_length=120, verbose_name="Horario")

    class Meta:
        verbose_name = "Cajero"
        verbose_name_plural = "Cajeros"

    def __str__(self):
        return f"Cajero: {self.usuario}"


class Notificacion(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("enviada", "Enviada"),
        ("leida", "Leída"),
        ("error", "Error"),
    )
    TIPOS = (
        ("info", "Información"),
        ("alerta", "Alerta"),
        ("promocion", "Promoción"),
        ("sistema", "Sistema"),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-fecha_envio"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.usuario} - {self.estado}"


# =========================
#  Clientes y catálogo
# =========================

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="cliente")
    nit_ci = models.CharField(max_length=30, unique=True, verbose_name="NIT/CI")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nit_ci} ({self.usuario or 'Sin usuario'})"


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    color = models.CharField(max_length=40, blank=True)
    talla = models.CharField(max_length=20, blank=True)
    codigo = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.codigo} ({self.categoria})"


class MovimientoStock(models.Model):
    TIPOS = (
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos")
    cantidad = models.IntegerField(help_text="Positivo para entrada, negativo para salida si corresponde")
    fecha = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=10, choices=TIPOS)

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.cantidad} de {self.producto} @ {self.fecha:%Y-%m-%d}"


# =========================
#  Carrito
# =========================

class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name="carrito")
    cantidad = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.cliente}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Ítem de Carrito"
        verbose_name_plural = "Ítems de Carrito"
        unique_together = ("carrito", "producto")

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"


# =========================
#  Ventas
# =========================

class Venta(models.Model):
    TIPOS_PAGO = (
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("transferencia", "Transferencia"),
        ("mixto", "Mixto"),
    )
    ESTADOS = (
        ("borrador", "Borrador"),
        ("confirmada", "Confirmada"),
        ("anulada", "Anulada"),
    )

    fecha_venta = models.DateTimeField(default=timezone.now)
    tipo_pago = models.CharField(max_length=20, choices=TIPOS_PAGO)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ventas", null=True, blank=True)
    cajero = models.ForeignKey(Cajero, on_delete=models.PROTECT, related_name="ventas")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha_venta"]

    def __str__(self):
        return f"Venta #{self.pk} - {self.fecha_venta:%Y-%m-%d} - {self.estado}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_venta")
    cantidad = models.PositiveIntegerField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"{self.cantidad} x {self.producto} (Venta #{self.venta_id})"
