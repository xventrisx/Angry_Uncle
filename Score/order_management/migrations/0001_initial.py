# Generated by Django 2.2.6 on 2021-04-09 13:07

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('date_created', models.DateField(auto_now=True)),
                ('cost', models.FloatField()),
                ('status', models.CharField(choices=[('P', 'В ОБРАБОТЕ'), ('PAID', 'ОПЛАЧЕН'), ('NO', 'ОТКЛОНЬОН'), ('READY', 'ГОТОВ К ВЫДАЧЕ')], max_length=5)),
                ('number', models.IntegerField(default=1)),
                ('cashier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateField(auto_now=True)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('last_activity', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True)),
                ('payment_made', models.FloatField(default=0)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_management.Order')),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_management.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_management.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop_assistant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oreders', to=settings.AUTH_USER_MODEL),
        ),
    ]