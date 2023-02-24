from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
def get_upload_path(instance, filename):
    return f"upload/{instance.user.id}/{filename}"

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to= get_upload_path)

    def __str__(self):
        return self.name
