# Generated by Django 2.2.2 on 2019-06-21 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comuscentia', '0006_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='msgs',
            field=models.IntegerField(default=0),
        ),
    ]
