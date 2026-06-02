"""
Gallery URLs
"""

from django.urls import path
from .views import (
    PublicGalleryListView, MyGalleryListView,
    GalleryUploadView, GalleryDetailView,
    GalleryPendingListView, GalleryApproveView,
    SpecialistGalleryView,
)

urlpatterns = [
    path("public/", PublicGalleryListView.as_view(), name="public_gallery"),
    path("my/", MyGalleryListView.as_view(), name="my_gallery"),
    path("upload/", GalleryUploadView.as_view(), name="gallery_upload"),
    path("<int:pk>/", GalleryDetailView.as_view(), name="gallery_detail"),
    path("pending/", GalleryPendingListView.as_view(), name="gallery_pending"),
    path("<int:pk>/approve/", GalleryApproveView.as_view(), name="gallery_approve"),
    path("specialist/<int:specialist_id>/", SpecialistGalleryView.as_view(), name="specialist_gallery"),
]
