# Generated by Django 4.0.4 on 2022-05-15 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_alter_persona_cel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='idpersona',
            new_name='idPersona',
        ),
    ]
