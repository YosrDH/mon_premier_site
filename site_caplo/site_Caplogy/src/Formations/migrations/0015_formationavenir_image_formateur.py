# Generated by Django 3.1.6 on 2024-07-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formations', '0014_formationavenir_nom_formateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='formationavenir',
            name='image_formateur',
            field=models.ImageField(default='', upload_to='fichiers/'),
            preserve_default=False,
        ),
    ]