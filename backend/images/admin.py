from django.contrib import admin

from .models import Image, ImageCategory


@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
