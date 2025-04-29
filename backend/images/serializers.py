from rest_framework import serializers

from .models import Image, ImageCategory


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "image", "category", "description", "created_at"]


class ImageCategorySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = ImageCategory
        fields = ["id", "name", "description", "images"]
