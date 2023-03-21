from rest_framework import serializers

from .models import Item


class ItemByuSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    price = serializers.FloatField()

