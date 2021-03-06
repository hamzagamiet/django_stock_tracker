# Generated by Django 3.2.6 on 2021-08-08 17:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_auto_20210808_1807"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
