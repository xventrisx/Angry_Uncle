# Generated by Django 2.2.6 on 2021-04-21 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0002_auto_20210416_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_management.Product'),
        ),
    ]