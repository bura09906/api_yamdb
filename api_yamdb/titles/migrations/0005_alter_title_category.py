# Generated by Django 3.2 on 2023-12-07 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20231206_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='title', to='titles.category', verbose_name='Категория'),
        ),
    ]
