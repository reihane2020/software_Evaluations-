# Generated by Django 3.2.9 on 2022-02-12 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0100_auto_20220212_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='software',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.software'),
        ),
    ]
