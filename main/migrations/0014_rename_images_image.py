# Generated by Django 3.2.9 on 2021-12-05 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_image_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
