# Generated by Django 5.0.4 on 2024-05-06 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appReRu', '0017_product_availability_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='original_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
