# Generated by Django 3.2.6 on 2021-08-13 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_auto_20210813_0414"),
    ]

    operations = [
        migrations.RenameField(
            model_name="watchlist",
            old_name="ticker",
            new_name="stock",
        ),
    ]