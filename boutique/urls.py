from django.urls import path, include
from rest_framework import routers
from . import views

# api versioning
router = routers.DefaultRouter()
router.register(r'roles', views.RolView, 'roles')
router.register(r'usuarios', views.UsuarioView, 'usuarios')
router.register(r'administradores', views.AdministradorView, 'administradores')
router.register(r'cajeros', views.CajeroView, 'cajeros')
router.register(r'notificaciones', views.NotificacionView, 'notificaciones')
router.register(r'clientes', views.ClienteView, 'clientes')
router.register(r'categorias', views.CategoriaView, 'categorias')
router.register(r'productos', views.ProductoView, 'productos')
router.register(r'movimientos-stock', views.MovimientoStockView, 'movimientos-stock')
router.register(r'carritos', views.CarritoView, 'carritos')
router.register(r'carrito-items', views.CarritoItemView, 'carrito-items')
router.register(r'ventas', views.VentaView, 'ventas')
router.register(r'detalles-venta', views.DetalleVentaView, 'detalles-venta')

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
