# Generated by Django 4.0.5 on 2022-08-02 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0003_alter_software_evaluations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='software',
            name='evaluations',
        ),
    ]
