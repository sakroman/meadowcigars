# Generated by Django 4.2.3 on 2023-08-03 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_category_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
