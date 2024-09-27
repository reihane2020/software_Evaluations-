# Generated by Django 4.0.5 on 2022-12-07 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
        ('authentication', '0015_account_documents_alter_account_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='documents',
        ),
        migrations.AddField(
            model_name='account',
            name='document1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document1', to='upload.image'),
        ),
        migrations.AddField(
            model_name='account',
            name='document2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document2', to='upload.image'),
        ),
        migrations.AddField(
            model_name='account',
            name='document3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document3', to='upload.image'),
        ),
    ]
