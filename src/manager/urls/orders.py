from django.urls import path

from manager import views

urlpatterns = [
    path("<int:product_id>/orders/", views.order_list_view, name="manager_orders_list"),
    path("<int:product_id>/orders/create", views.order_create_view, name="manager_orders_create"),
    path(
        "orders/<int:order_id>/update/to_shipping",
        views.update_order_status_to_shipping_view,
        name="manager_orders_update_status_to_shipping",
    ),
    path(
        "orders/<int:order_id>/update/to_completed",
        views.update_order_status_to_completed_view,
        name="manager_orders_update_status_to_completed",
    ),
    path(
        "orders/<int:order_id>/update/to_canceled",
        views.update_order_status_to_canceled_view,
        name="manager_orders_update_status_to_canceled",
    ),
]
