# Generated by Django 4.0.2 on 2022-04-14 06:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_order_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='final_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
                ('rate', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
