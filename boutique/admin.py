from django.contrib import admin
from boutique.models import (
    Rol, Usuario, Administrador, Cajero, Notificacion,
    Cliente, Categoria, Producto, MovimientoStock,
    Carrito, CarritoItem, Venta, DetalleVenta
)
# Register your models here.
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Cajero)
admin.site.register(Notificacion)
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MovimientoStock)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
