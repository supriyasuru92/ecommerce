from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import include, path


router = DefaultRouter()
router.register("customers", CustomersViewSet)
router.register("products", ProductsViewSet)
router.register("orders", OrdersViewSet)


urlpatterns = [
    path("", include(router.urls)),
]