# Generated by Django 2.2 on 2019-06-03 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comuscentia', '0004_auto_20190521_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='close',
        ),
    ]