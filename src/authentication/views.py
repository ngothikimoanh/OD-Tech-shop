from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect, render
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token

from authentication.decorators import login_required, not_login_required
from authentication.forms import LoginForm, ProfileForm, RegisterForm
from authentication.models import User


@not_login_required
def login_view(request: HttpRequest):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request=request, user=form.user)
            return render(request, "redirect_to.html")

        messages.error(request, "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "authentication/login.html", {"form": form})


@not_login_required
def register_view(request: HttpRequest):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return render(request, "redirect_to.html")

        messages.error(request, "Đăng ký thất bại, vui lòng kiểm tra lại thông tin.")

    is_exist_user = User.objects.exists()

    context = {
        "form": form,
        "is_exist_user": is_exist_user,
    }

    return render(request, "authentication/register.html", context)


@not_login_required
def login_with_google_view(request: HttpRequest):
    authorization_url, _ = settings.GOOGLE_FLOW.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )
    return redirect(authorization_url)


@not_login_required
def google_callback_view(request: HttpRequest):
    try:
        code = request.GET.get("code")
        settings.GOOGLE_FLOW.fetch_token(code=code)

        credentials = settings.GOOGLE_FLOW.credentials

        google_request = Request()

        id_token = credentials.id_token
        id_info = verify_oauth2_token(id_token, google_request)

        email = id_info["email"]
        user = User.objects.filter(email=email).first()

        if user:
            login(request=request, user=user)
            return render(request, "authentication/login.html")

        messages.error(request, "Tài khoản Google này chưa được đăng ký.")
    except Exception as exc:
        print("An error occurred while logging in with Google: ", exc)
        messages.error(request, "Có lỗi xảy ra khi đăng nhập bằng Google, vui lòng thử lại sau.")
    return redirect("auth_login")


@login_required
def profile_view(request: HttpRequest):
    user = User.objects.get(id=request.user.id)  # type: ignore
    form = ProfileForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công.")
            return redirect("auth_profile")

        messages.error(request, "Cập nhật thông tin thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "authentication/profile.html", {"form": form})
