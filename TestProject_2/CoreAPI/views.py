from django.shortcuts import render
from rest_framework import generics
from .models import User, StorageEncode, StorageDecode, StorageReceive
from .serializers import UserSerializer, StorageEncodeSerializer, StorageDecodeSerializer, StorageReceiveSerializer
from rest_framework.parsers import FileUploadParser
from django.http import FileResponse, HttpResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED
import rsa
# Create your views here.


class ListUserView(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer

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
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)
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
        (user.rsa_public_key, user.rsa_private_key) = rsa.newkeys(512)
        user.save()
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
        return super().post(request, *args, **kwargs)


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
                'Authentication token missing', code=HTTP_401_UNAUTHORIZED)
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
        return super().post(request, *args, **kwargs)


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
