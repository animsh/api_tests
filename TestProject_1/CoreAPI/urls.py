from django.urls import path
from .views import CustomUserView, UploadView, SingleUploadView

urlpatterns = [
    path('customusers/', CustomUserView.as_view()),
    path('upload/', UploadView.as_view(), name='upload'),
    path('upload/<int:pk>', SingleUploadView.as_view(), name='upload'),
]