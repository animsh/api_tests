from django.shortcuts import render
from rest_framework import generics
from .models import User, StorageEncode, StorageDecode, StorageReceive
from .serializers import UserSerializer, ListUserSerializer, StorageEncodeSerializer, StorageDecodeSerializer, StorageReceiveSerializer
from rest_framework.parsers import FileUploadParser
from django.http import FileResponse, HttpResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED
import rsa
from django.core.files import File
from .utils import hybrid_cryprography
import os
from django.conf import settings
import asyncio
# Create your views here.


class ListUserView(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = ListUserSerializer

    def get_queryset(self):
        token = self.request.META.get('HTTP_TOKEN')
        if token:
            user = User.objects.filter(token=token).first()
            if user:
                return User.objects.all()
            else:
                return User.objects.none()
        else:
            return User.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            raise AuthenticationFailed(
                'Authentication token missing or user not found', code=HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AccessToken.for_user(user)
        user.token = str(token)
        public_key, private_key = rsa.newkeys(512)
        user.rsa_public_key = public_key.save_pkcs1().decode('utf-8')
        user.rsa_private_key = private_key.save_pkcs1().decode('utf-8')
        user.save()

        encode_folder_path = os.path.join(
            settings.MEDIA_ROOT, f'upload/{user.id}/encoded_files')
        decode_folder_path = os.path.join(
            settings.MEDIA_ROOT, f'upload/{user.id}/decoded_files')
        key_folder_path = os.path.join(
            settings.MEDIA_ROOT, f'upload/{user.id}/key_files')

        if not os.path.exists(encode_folder_path):
            os.makedirs(encode_folder_path)

        if not os.path.exists(decode_folder_path):
            os.makedirs(decode_folder_path)

        if not os.path.exists(key_folder_path):
            os.makedirs(key_folder_path)

        return Response({
            'user': serializer.data,
            'token': user.token,
        })


class StorageEncodeView(generics.CreateAPIView):
    queryset = StorageEncode.objects.all()
    serializer_class = StorageEncodeSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            raise AuthenticationFailed(
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            raise AuthenticationFailed(
                'Invalid token', code=HTTP_401_UNAUTHORIZED)

        request.user = user
        response = super().post(request, *args, **kwargs)
        filepath = response.data['hidden_file'].replace(
            'http://127.0.0.1:8000/', '')
        hidden_file = open(os.path.join(settings.MEDIA_ROOT, filepath), 'rb')
        print(hidden_file)

        filepath = response.data['cover_file'].replace(
            'http://127.0.0.1:8000/', '')
        cover_file = open(os.path.join(settings.MEDIA_ROOT, filepath), 'rb')
        print(cover_file)

        hybrid_cryprography.encrypt_file(
            hidden_file, user.rsa_public_key, user.id, response.data['id'], response.data['cover_file_type'],cover_file)

        return response


class ListStorageEncodeView(generics.ListAPIView):
    # queryset = StorageEncode.objects.all()
    serializer_class = StorageEncodeSerializer
    parser_class = (FileUploadParser,)

    def get_queryset(self):
        token = self.request.META.get('HTTP_TOKEN')
        user = User.objects.filter(token=token).first()
        if user:
            return StorageEncode.objects.filter(user=user)
        else:
            return StorageEncode.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise AuthenticationFailed(
                'Authentication token missing or user not found or storage files not found', code=HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SingleStorageEncodeView(generics.RetrieveAPIView):
    queryset = StorageEncode.objects.all()
    serializer_class = StorageEncodeSerializer

    def get(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            raise AuthenticationFailed(
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            raise AuthenticationFailed(
                'Invalid token', code=HTTP_401_UNAUTHORIZED)

        request.user = user
        return super().get(request, *args, **kwargs)


class StorageDecodeView(generics.CreateAPIView):
    queryset = StorageDecode.objects.all()
    serializer_class = StorageDecodeSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            raise AuthenticationFailed(
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            raise AuthenticationFailed(
                'Invalid token', code=HTTP_401_UNAUTHORIZED)

        request.user = user
        response = super().post(request, *args, **kwargs)
        filepath = response.data['encoded_file'].replace(
            'http://127.0.0.1:8000/', '')
        f = open(os.path.join(settings.MEDIA_ROOT, filepath), 'rb')
        print(f)

        hybrid_cryprography.decrypt_file(
            user.id, f, request.data['encrypted_password'], user.rsa_private_key, response.data['id'])

        return response


class SingleStorageDecodeView(generics.RetrieveAPIView):
    queryset = StorageDecode.objects.all()
    serializer_class = StorageDecodeSerializer

    def get(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            raise AuthenticationFailed(
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            raise AuthenticationFailed(
                'Invalid token', code=HTTP_401_UNAUTHORIZED)

        request.user = user
        return super().get(request, *args, **kwargs)


class StorageReceiveView(generics.ListCreateAPIView):
    queryset = StorageReceive.objects.all()
    serializer_class = StorageReceiveSerializer

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            raise AuthenticationFailed(
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            raise AuthenticationFailed(
                'Invalid token', code=HTTP_401_UNAUTHORIZED)

        request.user = user
        return super().post(request, *args, **kwargs)
