from django.db import models


class ImageCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(
        ImageCategory, on_delete=models.CASCADE, related_name="images"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
