# Generated by Django 4.0.2 on 2022-04-14 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='company',
        ),
    ]
