import os
from django.conf import settings


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

