# Generated by Django 4.0.4 on 2022-06-18 23:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_descripción_product_descripcion_delete_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mods',
            name='user',
        ),
        migrations.AddField(
            model_name='mods',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
