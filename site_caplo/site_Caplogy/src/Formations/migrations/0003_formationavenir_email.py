# Generated by Django 3.1.6 on 2024-07-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formations', '0002_remove_formationavenir_adresse_mail_organisateurs'),
    ]

    operations = [
        migrations.AddField(
            model_name='formationavenir',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]