# Generated by Django 3.2 on 2023-11-27 18:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_confirmationcode_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_code', to=settings.AUTH_USER_MODEL),
        ),
    ]
