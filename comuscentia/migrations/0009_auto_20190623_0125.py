# Generated by Django 2.2.2 on 2019-06-22 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comuscentia', '0008_auto_20190623_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='textblock',
            field=models.TextField(default='Text field for learning stuff. We advice to start with a link to the chat.'),
        ),
    ]
