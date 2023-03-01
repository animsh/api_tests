import os
from django.conf import settings
import rsa
from Crypto.Cipher import AES
from ..models import StorageDecode
import base64
import datetime


def path_to_hidden_file(userid, filename):
    return os.path.join(
        settings.MEDIA_ROOT, f"upload/{userid}/hidden_files/{filename}")


def path_to_cover_file(userid, filename):
    return os.path.join(
        settings.MEDIA_ROOT, f"upload/{userid}/cover_files/{filename}")


def path_to_encoded_file(userid, filename):
    return os.path.join(
        settings.MEDIA_ROOT, f"upload/{userid}/encoded_files/{filename}")


def path_to_decoded_file(userid, filename):
    return os.path.join(
        settings.MEDIA_ROOT, f"upload/{userid}/decoded_files/{filename}")


def decrypt_file_and_save(userid, encrypted_password, private_key, encoded_file, storage_id):
    filename = encoded_file.name.split('/')[-1]
    extension = filename.split('.')[-1]
    name = filename.split('.')[0]
    print(filename)

    file_in = open(path_to_decoded_file(userid, filename), "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    file_in.close()
    print("hii")
    # print(base64.b64decode(encrypted_password).encode('utf-8'),
    #       rsa.PrivateKey.load_pkcs1(private_key))
    decoded = base64.b64decode(encrypted_password.encode())
    print("dec: ", decoded)
    key = rsa.decrypt(decoded,
                      rsa.PrivateKey.load_pkcs1(private_key))
    print("key: ", key)

    # key = rsa.decrypt(base64.b64decode(encrypted_password.encode('utf-8')),
    #                   rsa.PrivateKey.load_pkcs1(private_key))
    # print(key)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    actualname = name + \
        str(datetime.datetime.now().microsecond) + "." + extension
    with open(path_to_decoded_file(userid, actualname), 'wb') as f2:
        f2.write(data)
        StorageDecode.objects.filter(id=storage_id).update(
            decoded_file=path_to_decoded_file(userid, actualname))
