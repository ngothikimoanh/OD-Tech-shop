import re

from django.core.validators import RegexValidator
from django.db import models

from authentication.models import User
from authentication.validators import validate_phone_number
from common.models import TimestampMixin
from manager.utils import product_image_path


class Product(TimestampMixin):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    thumbnail_image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)


class Attribute(TimestampMixin):
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=100, null=True, blank=True)


class ProductAttribute(TimestampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class Device(TimestampMixin):
    sku = models.AutoField(primary_key=True)
    imei = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                regex="^[0-9]{15}$",
                message="IMEI phải có 15 hoặc 16 chữ số.",
            )
        ],
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(TimestampMixin):
    buyer_phone_numbers = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex="^0[0-9]{9,10}$",
                message="Số điện thoại không hợp lệ.",
            )
        ],
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Đang chờ"),
            ("shipping", "Đang giao"),
            ("completed", "Đã giao"),
            ("canceled", "Đã hủy"),
        ],
        default="pending",
    )
    address = models.CharField(null=True, blank=True, max_length=500)
