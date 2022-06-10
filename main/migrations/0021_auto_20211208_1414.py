# Generated by Django 3.2.9 on 2021-12-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20211208_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد ')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی ')),
            ],
        ),
        migrations.RemoveField(
            model_name='metric',
            name='metric_class',
        ),
    ]
