# Generated by Django 4.0.4 on 2022-05-29 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0007_remove_persona_activation_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_code', models.CharField(max_length=254)),
            ],
        ),
    ]
