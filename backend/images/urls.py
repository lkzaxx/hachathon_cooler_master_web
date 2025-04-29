from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentGenerateImageView,
    BedrockAgentView,
    GenerateImagesView,
    ImageCategoryViewSet,
    ImageViewSet,
    upload_reference_image,
)

router = DefaultRouter()
router.register(r"images", ImageViewSet)
router.register(r"categories", ImageCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", upload_reference_image, name="upload_image"),
    path(
        "agent-generate-image/",
        AgentGenerateImageView.as_view(),
        name="agent-generate-image",
    ),
    path("agent/", BedrockAgentView.as_view(), name="bedrock-agent"),
    path("generate-images/", GenerateImagesView.as_view(), name="generate-images"),
]
