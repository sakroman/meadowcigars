# Generated by Django 4.2.3 on 2023-08-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_shippinginfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippinginfo',
            name='city',
            field=models.CharField(default=4, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='phone_number',
            field=models.CharField(default=4, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='postcode',
            field=models.CharField(default=4, max_length=12),
            preserve_default=False,
        ),
    ]
