# Generated by Django 4.1.7 on 2023-02-23 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoreAPI', '0003_remove_uploadmodel_userid_uploadmodel_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadModel',
            new_name='Upload',
        ),
        migrations.RenameModel(
            old_name='CustomUserModel',
            new_name='User',
        ),
    ]
