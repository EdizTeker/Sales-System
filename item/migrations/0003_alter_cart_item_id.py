# Generated by Django 4.2.14 on 2024-07-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item_id',
            field=models.PositiveIntegerField(),
        ),
    ]
