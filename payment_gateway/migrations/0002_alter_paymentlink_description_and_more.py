# Generated by Django 4.2.16 on 2024-09-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlink',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentlink',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
    ]
