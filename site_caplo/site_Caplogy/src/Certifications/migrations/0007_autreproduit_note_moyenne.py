# Generated by Django 3.1.7 on 2024-07-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Certifications', '0006_auto_20240722_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='autreproduit',
            name='note_moyenne',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
