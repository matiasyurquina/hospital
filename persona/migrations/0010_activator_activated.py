# Generated by Django 4.0.4 on 2022-05-29 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0009_alter_activator_activation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='activator',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
