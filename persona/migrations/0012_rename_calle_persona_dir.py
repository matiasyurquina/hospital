# Generated by Django 4.2.4 on 2023-08-24 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0011_activator_activation_code_encoded'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='calle',
            new_name='dir',
        ),
    ]
