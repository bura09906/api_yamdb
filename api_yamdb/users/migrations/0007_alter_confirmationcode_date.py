# Generated by Django 3.2 on 2023-11-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_confirmationcode_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
