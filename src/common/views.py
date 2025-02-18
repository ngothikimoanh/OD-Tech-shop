from django.shortcuts import redirect, render

from authentication.models import User
from manager.models import Product


def home_view(request):
    if not User.objects.exists():
        return redirect("auth_register")

    products = Product.objects.all()

    return render(request, "home.html", {"products": products})
