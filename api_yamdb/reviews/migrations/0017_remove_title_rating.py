# Generated by Django 3.2 on 2023-12-06 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20231207_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
