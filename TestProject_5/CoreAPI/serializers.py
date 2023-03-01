from rest_framework import serializers
from .models import User, StorageEncode, StorageDecode, StorageReceive


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password',
                  'token', 'rsa_public_key', 'rsa_private_key')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password',
                  'token', 'rsa_public_key', 'rsa_private_key')


class StorageEncodeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    encoded_file = serializers.CharField(read_only=True)
    encrypted_password = serializers.CharField(read_only=True)
    key_file = serializers.CharField(read_only=True)

    class Meta:
        model = StorageEncode
        fields = ('id', 'user', 'user_id', 'cover_file', 'cover_file_type',
                  'hidden_file', 'encoded_file', 'public_key_of_receiver', 'encrypted_password', 'key_file')


class StorageDecodeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    decoded_file = serializers.CharField(read_only=True)

    class Meta:
        model = StorageDecode
        fields = ('id', 'user', 'user_id', 'encoded_file', 'encoded_file_type',
                  'decoded_file', 'encrypted_password', 'key_file', 'private_key')


class StorageReceiveSerializer(serializers.ModelSerializer):
    fromuser = UserSerializer(read_only=True)
    fromuser_id = serializers.IntegerField(write_only=True)
    touser = UserSerializer(read_only=True)
    touser_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StorageReceive
        fields = ('id', 'fromuser', 'fromuser_id', 'touser',
                  'touser_id', 'encoded_file', 'password')
