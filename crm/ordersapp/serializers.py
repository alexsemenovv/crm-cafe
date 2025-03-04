from typing import Tuple

from django.db.models import Model
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Order
        fields: Tuple[str] = (
            "pk",
            "table_number",
            "items",
            "status",
            "total_price",
        )
