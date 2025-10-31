from rest_framework import serializers
from .models import (
    Rol, Usuario, Administrador, Cajero, Notificacion,
    Cliente, Categoria, Producto, MovimientoStock,
    Carrito, CarritoItem, Venta, DetalleVenta
)
from django.contrib.auth.models import User


# =========================
#  Serializadores base
# =========================

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "is_staff"]


class UsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    roles = RolSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "user", "nombre", "apellido", "roles"]


class AdministradorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Administrador
        fields = ["id", "usuario"]


class CajeroSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Cajero
        fields = ["id", "usuario", "horario"]


class NotificacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Notificacion
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ["id", "usuario", "nit_ci"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ["id", "categoria", "color", "talla", "codigo", "stock"]


class MovimientoStockSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = MovimientoStock
        fields = ["id", "producto", "cantidad", "fecha", "tipo"]


# =========================
#  Carrito
# =========================

class CarritoItemSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = CarritoItem
        fields = ["id", "producto", "cantidad"]


class CarritoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    items = CarritoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Carrito
        fields = ["id", "cliente", "cantidad", "fecha_actualizacion", "items"]


# =========================
#  Venta y Detalle de Venta
# =========================

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ["id", "producto", "cantidad", "costo", "subtotal"]


class VentaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cajero = CajeroSerializer(read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id",
            "fecha_venta",
            "tipo_pago",
            "total",
            "estado",
            "cliente",
            "cajero",
            "detalles",
        ]
# =========================