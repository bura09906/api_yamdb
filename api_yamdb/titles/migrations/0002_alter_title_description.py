# Generated by Django 3.2 on 2023-11-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание'),
        ),
    ]
