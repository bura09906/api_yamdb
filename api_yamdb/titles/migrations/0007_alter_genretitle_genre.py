# Generated by Django 3.2 on 2023-12-09 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0006_alter_title_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='titles.genre'),
        ),
    ]
