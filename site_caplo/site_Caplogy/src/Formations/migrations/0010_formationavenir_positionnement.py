# Generated by Django 3.1.6 on 2024-07-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formations', '0009_formationavenir_public_visé'),
    ]

    operations = [
        migrations.AddField(
            model_name='formationavenir',
            name='Positionnement',
            field=models.TextField(default=''),
        ),
    ]
