# Generated by Django 4.2.6 on 2023-10-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorsapp', '0003_alter_author_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='goodreads_url',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
