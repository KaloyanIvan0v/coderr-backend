# Generated by Django 4.2 on 2025-04-29 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, max_length=255)),
                ('profile_image', models.FileField(blank=True, upload_to='profile_files/')),
                ('location', models.CharField(blank=True, max_length=255)),
                ('tel', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('working_hours', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='main_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
