from django.urls import include, path

urlpatterns = [
    path("products/", include("manager.urls.products")),
    path("employees/", include("manager.urls.employees")),
    path("orders/", include("manager.urls.orders")),
]
