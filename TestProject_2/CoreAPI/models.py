from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    rsa_public_key = models.CharField(max_length=1000, default="")
    rsa_private_key = models.CharField(max_length=1000, default="")
    token = models.CharField(max_length=1000, default="")

    def __str__(self):
        return '__all__'


def get_hidded_file_upload_path(instance, filename):
    return f"upload/{instance.user.id}/hidden_files/{filename}"


def get_cover_file_upload_path(instance, filename):
    return f"upload/{instance.user.id}/cover_files/{filename}"


def get_encoded_file_upload_path(instance, filename):
    return f"upload/{instance.user.id}/encoded_files/{filename}"


def get_decoded_file_upload_path(instance, filename):
    return f"upload/{instance.user.id}/decoded_files/{filename}"


class StorageEncode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    hidded_file = models.FileField(upload_to=get_hidded_file_upload_path)
    cover_file = models.FileField(upload_to=get_cover_file_upload_path)
    encoded_file = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return '__all__'


class StorageDecode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    encoded_file = models.FileField(upload_to=get_encoded_file_upload_path)
    decoded_file = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return '__all__'


class StorageReceive(models.Model):
    fromuser = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='fromuser')
    touser = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='touser')
    encoded_file = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return '__all__'
