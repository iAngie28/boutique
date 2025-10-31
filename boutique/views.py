from django.shortcuts import render
from django.shortcuts import render  # (no se usa, pero lo dejo para respetar tu plantilla)
from rest_framework import viewsets

from .serializer import (
    RolSerializer, UsuarioSerializer, AdministradorSerializer, CajeroSerializer, NotificacionSerializer,
    ClienteSerializer, CategoriaSerializer, ProductoSerializer, MovimientoStockSerializer,
    CarritoSerializer, CarritoItemSerializer, VentaSerializer, DetalleVentaSerializer
)
from .models import (
    Rol, Usuario, Administrador, Cajero, Notificacion,
    Cliente, Categoria, Producto, MovimientoStock,
    Carrito, CarritoItem, Venta, DetalleVenta
)


class RolView(viewsets.ModelViewSet):
    serializer_class = RolSerializer
    queryset = Rol.objects.all()


class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()


class AdministradorView(viewsets.ModelViewSet):
    serializer_class = AdministradorSerializer
    queryset = Administrador.objects.all()


class CajeroView(viewsets.ModelViewSet):
    serializer_class = CajeroSerializer
    queryset = Cajero.objects.all()


class NotificacionView(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all()


class ClienteView(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()


class CategoriaView(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()


class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()


class MovimientoStockView(viewsets.ModelViewSet):
    serializer_class = MovimientoStockSerializer
    queryset = MovimientoStock.objects.all()


class CarritoView(viewsets.ModelViewSet):
    serializer_class = CarritoSerializer
    queryset = Carrito.objects.all()


class CarritoItemView(viewsets.ModelViewSet):
    serializer_class = CarritoItemSerializer
    queryset = CarritoItem.objects.all()


class VentaView(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()


class DetalleVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()
