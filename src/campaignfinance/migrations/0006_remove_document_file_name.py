# Generated by Django 4.2.2 on 2023-07-11 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaignfinance', '0005_rename_relationship_notes_relationship_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file_name',
        ),
    ]
