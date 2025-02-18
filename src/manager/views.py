from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from authentication.constants import Role
from authentication.models import User
from manager.form import AttributeValueForm, ProductForm
from manager.models import Device, Order, Product, ProductAttribute


def products_create_view(request: HttpRequest):
    form = ProductForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("manager_products_list")
    return render(request, "manager/products_create.html", {"form": form})


def products_list_view(request: HttpRequest):
    products = Product.objects.all()
    return render(request, "manager/products_list.html", {"products": products})


def products_update_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, files=request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("manager_products_list")

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "manager/products_update.html", context)


def products_update_remove_thumbnail_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product.thumbnail_image.delete()
    return redirect("manager_products_update", product_id=product_id)


def products_delete_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("manager_products_list")


def device_list_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    devices = Device.objects.filter(product=product)

    context = {
        "devices": devices,
        "product": product,
    }
    return render(request, "manager/devices_list.html", context)


def device_create_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    data = request.POST

    try:
        Device.objects.create(
            imei=data.get("imei"),
            product=product,
        )
    except Exception:
        messages.error(request, "Error creating device")

    devices = Device.objects.filter(product=product)

    context = {
        "devices": devices,
        "product": product,
    }

    return render(request, "manager/devices_list.html", context)


def products_create_attributes_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    product_attributes = ProductAttribute.objects.filter(product=product).select_related("attribute")

    form = AttributeValueForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save(product=product)
            return redirect("manager_products_list")
    context = {
        "form": form,
        "product": product,
        "product_attributes": product_attributes,
    }

    return render(request, "manager/create_attributes.html", context)


def employee_list_view(request: HttpRequest):
    employees = User.objects.filter(role=Role.EMPLOYEE)
    return render(request, "employee/employee_list.html", {"employees": employees})


def employee_create_view(request: HttpRequest):
    if request.method == "POST":
        try:
            user = User.objects.get(phone_number=request.POST.get("phone_number"))
        except User.DoesNotExist:
            user = None
        if user:
            if not user.username and not user.email:
                messages.error(request, "Người dùng cần có tên và email")
                return redirect("manager_employees_create")
            else:
                user.role = Role.EMPLOYEE
                user.save()
                messages.success(request, "Tạo nhân viên thành công")
                return redirect("manager_employees_list")
        else:
            messages.error(request, "Người dùng không tồn tại")
            return redirect("manager_employees_create")
    return render(request, "employee/employee_create.html")


def order_list_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    oders = Order.objects.filter(product=product)

    context = {
        "oders": oders,
        "product": product,
    }
    return render(request, "orders/orders_list.html", context)


def order_create_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    data = request.POST
    if request.method == "POST":
        try:
            Order.objects.create(
                buyer_phone_numbers=data.get("buyer_phone_numbers"),
                seller=request.user,
                product=product,
                value=product.price,
                status="pending",
                address=data.get("address"),
            )
        except Exception:
            messages.error(request, "Error creating order")

    orders = Order.objects.filter(product=product)

    context = {
        "orders": orders,
        "product": product,
    }

    return render(request, "orders/orders_list.html", context)


def product_detail_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    product_attributes = ProductAttribute.objects.filter(product=product).select_related("attribute")

    return render(
        request, "manager/product_detail.html", {"product": product, "product_attributes": product_attributes}
    )


def update_order_status_to_shipping_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    order.status = "shipping"
    order.save()

    return redirect("home")


def update_order_status_to_completed_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    order.status = "completed"
    order.save()

    return redirect("home")


def update_order_status_to_canceled_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    order.status = "canceled"
    order.save()

    return redirect("home")
