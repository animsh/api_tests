from django.shortcuts import render
from rest_framework import generics
from .models import User, Upload
from .serializers import UserSerializer, UploadSerializer
from rest_framework.parsers import FileUploadParser
from django.http import FileResponse

# Create your views here.


class CustomUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UploadView(generics.ListCreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    parser_class = (FileUploadParser,)


class SingleUploadView(generics.RetrieveAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
