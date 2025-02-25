from typing import Any

from django.template.defaulttags import register


@register.filter
def get_item(dictionary: dict | None, key: str) -> Any:
    return dictionary and dictionary.get(key)
