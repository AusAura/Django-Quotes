# Generated by Django 4.2.6 on 2023-10-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorsapp', '0002_alter_author_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.CharField(),
        ),
    ]
