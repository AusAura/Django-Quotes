# Generated by Django 4.2.6 on 2023-10-23 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='name',
            new_name='quote',
        ),
    ]