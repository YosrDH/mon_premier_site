# Generated by Django 3.1.7 on 2024-07-21 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Certifications', '0004_avis_produit_similaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='certification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Certifications.certification'),
        ),
    ]