# Generated by Django 4.1.7 on 2023-02-27 18:17

import CoreAPI.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('rsa_public_key', models.CharField(default='', max_length=1000)),
                ('rsa_private_key', models.CharField(default='', max_length=1000)),
                ('token', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='StorageReceive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoded_file', models.CharField(max_length=1000)),
                ('password', models.CharField(max_length=1000)),
                ('fromuser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fromuser', to='CoreAPI.user')),
                ('touser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='touser', to='CoreAPI.user')),
            ],
        ),
        migrations.CreateModel(
            name='StorageEncode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hidden_file', models.FileField(upload_to=CoreAPI.models.get_hidden_file_upload_path)),
                ('cover_file', models.FileField(upload_to=CoreAPI.models.get_cover_file_upload_path)),
                ('cover_file_type', models.CharField(choices=[('A', 'Audio'), ('V', 'Video'), ('I', 'Image')], max_length=1)),
                ('encoded_file', models.CharField(max_length=1000)),
                ('public_key_of_receiver', models.CharField(max_length=1000)),
                ('encrypted_password', models.CharField(max_length=1000)),
                ('key_file', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CoreAPI.user')),
            ],
        ),
        migrations.CreateModel(
            name='StorageDecode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoded_file', models.FileField(upload_to=CoreAPI.models.get_encoded_file_upload_path)),
                ('encoded_file_type', models.CharField(choices=[('A', 'Audio'), ('V', 'Video'), ('I', 'Image')], max_length=1)),
                ('decoded_file', models.CharField(max_length=1000)),
                ('encrypted_password', models.CharField(max_length=1000)),
                ('key_file', models.FileField(upload_to=CoreAPI.models.get_encoded_file_upload_path)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CoreAPI.user')),
            ],
        ),
    ]
