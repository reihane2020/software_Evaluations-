# Generated by Django 3.2.9 on 2021-12-20 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_auto_20211220_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='softwareevaluate',
            name='people',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='تعداد افراد'),
        ),
    ]
