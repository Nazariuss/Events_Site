# Generated by Django 4.1.3 on 2022-12-01 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]