from django.urls import path
from .views import ListUserView, ListStorageDecodeView, CreateUserView, SingleUserView, LoginUserView, StorageEncodeView, ListStorageEncodeView, SingleStorageEncodeView, StorageDecodeView, SingleStorageDecodeView, StorageReceiveView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('users', ListUserView.as_view(), name="users-all"),
    path('users/me', SingleUserView.as_view(), name="users-me"),
    path('users/signup', CreateUserView.as_view(), name="users-create"),
    path('users/login', LoginUserView.as_view(), name="users-login"),
    path('users/encodedfiles', ListStorageEncodeView.as_view(),
         name="storage-encode-all"),
    path('users/decodedfiles', ListStorageDecodeView.as_view(),
         name="storage-decode-all"),

    path('users/encode', StorageEncodeView.as_view(), name="storage-encode"),
    path('users/encode/<int:pk>', SingleStorageEncodeView.as_view(),
         name="storage-encode-single"),
    path('users/decode', StorageDecodeView.as_view(), name="storage-decode"),
    path('users/decode/<int:pk>', SingleStorageDecodeView.as_view(),
         name="storage-decode-single"),
    path('users/send', StorageReceiveView.as_view(), name="storage-receive"),

]
