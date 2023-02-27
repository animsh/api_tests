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
import json
# Create your views here.

TOKEN_MISSING = 'Authentication token missing'
USER_NOT_FOUND = 'User not found'
BASE_URL = 'http://127.0.0.1:8000/'


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer

    def list(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        response = super().list(request, *args, **kwargs)
        return Response({'status': 'success', 'message': 'list of users', 'data': response.data})


class LoginUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        print(body['email'])
        user = User.objects.filter(email=body['email']).first()
        print(user)

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        return Response({'status': 'success', 'message': 'login successfull', 'data': [{'user_id': user.id, 'token': user.token}]})


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
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
                'status': 'success',
                'user': serializer.data,
                'token': user.token,
            })
        except Exception as e:
            return Response({
                'status': 'failure',
                'message': dict(e.args[0])
            }, status=400)


class StorageEncodeView(generics.CreateAPIView):
    queryset = StorageEncode.objects.all()
    serializer_class = StorageEncodeSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        response = super().post(request, *args, **kwargs)

        filepath = response.data['hidden_file'].replace(BASE_URL, '')
        hidden_file = open(os.path.join(
            settings.MEDIA_ROOT, filepath), 'rb')
        print(hidden_file)

        filepath = response.data['cover_file'].replace(BASE_URL, '')
        cover_file = open(os.path.join(
            settings.MEDIA_ROOT, filepath), 'rb')
        print(cover_file)

        hybrid_cryprography.encrypt_file(
            hidden_file, user.rsa_public_key, user.id, response.data['id'], response.data['cover_file_type'], cover_file)

        return Response({'status': 'success', 'message': 'file encoded successfully', 'data': response.data})


class ListStorageEncodeView(generics.ListAPIView):
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

        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        if not queryset.exists():
            return Response({'status': 'failure', 'message': 'No data found', 'data': []})

        request.user = user
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'message': 'list of encoded files', 'data': serializer.data})


class SingleStorageEncodeView(generics.RetrieveAPIView):
    queryset = StorageEncode.objects.all()
    serializer_class = StorageEncodeSerializer

    def get(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        try:
            response = super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'status': 'failure', 'message': str(e), 'data': []})

        return Response({'status': 'success', 'message': 'encoded file details', 'data': response.data})


class StorageDecodeView(generics.CreateAPIView):
    queryset = StorageDecode.objects.all()
    serializer_class = StorageDecodeSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        try:
            request.user = user
            response = super().post(request, *args, **kwargs)
            filepath = response.data['encoded_file'].replace(BASE_URL, '')
            f = open(os.path.join(settings.MEDIA_ROOT, filepath), 'rb')
            print(f)

            hybrid_cryprography.decrypt_file(
                user.id, f, request.data['encrypted_password'], user.rsa_private_key, response.data['id'])
        except Exception as e:
            return Response({'status': 'failure', 'message': dict(e.args[0]), 'data': []})

        return Response({'status': 'success', 'message': 'file decoded successfully', 'data': response.data})


class SingleStorageDecodeView(generics.RetrieveAPIView):
    queryset = StorageDecode.objects.all()
    serializer_class = StorageDecodeSerializer

    def get(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        try:
            response = super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'status': 'failure', 'message': str(e), 'data': []})

        return Response({'status': 'success', 'message': 'decoded file details', 'data': response.data})


class StorageReceiveView(generics.ListCreateAPIView):
    queryset = StorageReceive.objects.all()
    serializer_class = StorageReceiveSerializer

    def list(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        try:
            response = super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'status': 'failure', 'message': str(e), 'data': []})

        return Response({'status': 'success', 'message': 'list of received files', 'data': response.data})

    def post(self, request, *args, **kwargs):
        if 'HTTP_TOKEN' not in request.META:
            return Response({'status': 'failure', 'message': TOKEN_MISSING, 'data': []})

        token = request.META['HTTP_TOKEN']
        user = User.objects.filter(token=token).first()

        if user is None:
            return Response({'status': 'failure', 'message': USER_NOT_FOUND, 'data': []})

        request.user = user
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({'status': 'failure', 'message': dict(e.args[0]), 'data': []})

        return Response({'status': 'success', 'message': 'file received successfully', 'data': response.data})
