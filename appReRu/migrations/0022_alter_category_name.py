# Generated by Django 5.0.4 on 2024-05-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appReRu', '0021_rename_details_product_details_1_product_details_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
