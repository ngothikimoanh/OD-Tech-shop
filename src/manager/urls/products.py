from django.urls import path

from manager import views

urlpatterns = [
    path("", views.products_list_view, name="manager_products_list"),
    path("<int:product_id>/detail/", views.product_detail_view, name="manager_products_detail"),
    path("create/", views.products_create_view, name="manager_products_create"),
    path("update/<int:product_id>", views.products_update_view, name="manager_products_update"),
    path(
        "update/remove_thumbnail/<int:product_id>",
        views.products_update_remove_thumbnail_view,
        name="manager_products_update_remove_thumbnail",
    ),
    path("delete/<int:product_id>", views.products_delete_view, name="manager_products_delete"),
    path(
        "<int:product_id>/attributes/", views.products_create_attributes_view, name="manager_products_create_attributes"
    ),
    # Devices
    path("<int:product_id>/devices", views.device_list_view, name="manager_devices_list"),
    path("<int:product_id>/devices/create", views.device_create_view, name="manager_devices_create"),
]
