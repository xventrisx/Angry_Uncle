# Generated by Django 2.2.6 on 2020-06-17 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('token', models.CharField(max_length=255)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasker.Project')),
            ],
        ),
    ]
