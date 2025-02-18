from django import forms

from authentication.models import User
from authentication.validators import validate_phone_number
from manager.models import Attribute, Order, Product, ProductAttribute


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "thumbnail_image", "category"]


class AttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = ["name", "group"]


class AttributeValueForm(forms.Form):
    attribute = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)

    def save(self, product: Product):
        data = self.cleaned_data

        attribute = data.get("attribute")
        value = data.get("value")

        attribute, _ = Attribute.objects.get_or_create(name=attribute)

        return ProductAttribute.objects.create(
            product=product,
            attribute=attribute,
            value=value,
        )


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["buyer_phone_numbers", "seller", "product", "value", "address", "status"]
