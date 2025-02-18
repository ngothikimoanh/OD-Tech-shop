from typing import Any

from django import forms
from django.contrib.auth.password_validation import validate_password

from authentication.models import User
from authentication.validators import validate_phone_number


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    password = forms.CharField(max_length=128)
    user: User | None = None

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        self.user = User.objects.filter(phone_number=phone_number).first()
        if not self.user:
            raise forms.ValidationError("Số điện thoại này chưa được đăng ký.", code="invalid")

        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password or (self.user and not self.user.check_password(raw_password=password)):
            raise forms.ValidationError("Mật khẩu không đúng. Vui lòng kiểm tra lại", code="invalid")

        return password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=128, validators=[validate_password])

    class Meta:
        model = User
        fields = ["phone_number", "password"]

    def save(self, commit: bool = True) -> Any:
        user_create_args = {
            "phone_number": self.cleaned_data.get("phone_number"),
            "password": self.cleaned_data.get("password"),
        }

        if not User.objects.exists():
            user = User.objects.create_superuser(**user_create_args)  # type: ignore
        else:
            user = User.objects.create_user(**user_create_args)  # type: ignore

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone_number", "email", "first_name", "last_name"]
