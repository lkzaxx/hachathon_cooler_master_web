from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import health_check, protected_media

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("images.urls")),
    path("protected-media/<path:key>/", protected_media, name="protected_media"),
    path("", health_check),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
