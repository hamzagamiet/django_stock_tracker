# Generated by Django 3.2.6 on 2021-08-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="market_cap",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="stock",
            name="price",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]