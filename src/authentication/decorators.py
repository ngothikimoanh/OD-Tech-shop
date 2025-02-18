from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect


def login_required(view_func):
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Bạn cần đăng nhập")
            return redirect("auth_login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def not_login_required(view_func):
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
