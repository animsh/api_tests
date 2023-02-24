from rest_framework import serializers
from .models import User, StorageEncode, StorageDecode, StorageReceive


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class StorageEncodeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    encoded_file = serializers.CharField(read_only=True)

    class Meta:
        model = StorageEncode
        fields = ('id', 'user', 'user_id', 'cover_file',
                  'hidded_file', 'encoded_file', 'password')


class StorageDecodeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    decoded_file = serializers.CharField(read_only=True)

    class Meta:
        model = StorageDecode
        fields = ('id', 'user', 'user_id', 'encoded_file',
                  'decoded_file', 'password')

class StorageReceiveSerializer(serializers.ModelSerializer):
    fromuser = UserSerializer(read_only=True)
    fromuser_id = serializers.IntegerField(write_only=True)
    touser = UserSerializer(read_only=True)
    touser_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StorageReceive
        fields = ('id', 'fromuser', 'fromuser_id', 'touser',
                  'touser_id', 'encoded_file', 'password')