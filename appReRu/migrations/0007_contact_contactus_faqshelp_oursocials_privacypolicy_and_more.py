# Generated by Django 5.0.4 on 2024-04-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appReRu', '0006_advertisement1_advertisement2_advertisement3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FaqsHelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_payment_made', models.TextField(blank=True, null=True)),
                ('help_how_paypal', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OurSocials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField(blank=True, max_length=150, null=True)),
                ('twitter', models.URLField(blank=True, max_length=150, null=True)),
                ('linkedin', models.URLField(blank=True, max_length=150, null=True)),
                ('youtube', models.URLField(blank=True, max_length=150, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]