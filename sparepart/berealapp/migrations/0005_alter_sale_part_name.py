# Generated by Django 4.2.4 on 2023-08-18 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berealapp', '0004_rename_item_name_product_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='part_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
