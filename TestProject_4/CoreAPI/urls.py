from django.urls import path
from .views import ListUserView, CreateUserView, LoginUserView, StorageEncodeView, ListStorageEncodeView, SingleStorageEncodeView, StorageDecodeView, SingleStorageDecodeView, StorageReceiveView

urlpatterns = [
    path('users', ListUserView.as_view(), name="users-all"),
    path('users/signup', CreateUserView.as_view(), name="users-create"),
    path('users/login', LoginUserView.as_view(), name="users-login"),
    path('users/encodedfiles', ListStorageEncodeView.as_view(),
         name="storage-encode-all"),

    path('users/encode', StorageEncodeView.as_view(), name="storage-encode"),
    path('users/encode/<int:pk>', SingleStorageEncodeView.as_view(),
         name="storage-encode-single"),
    path('users/decode', StorageDecodeView.as_view(), name="storage-decode"),
    path('users/decode/<int:pk>', SingleStorageDecodeView.as_view(),
         name="storage-decode-single"),
    path('users/send', StorageReceiveView.as_view(), name="storage-receive"),

]
