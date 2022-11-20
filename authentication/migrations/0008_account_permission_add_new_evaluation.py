# Generated by Django 4.0.5 on 2022-08-02 12:32

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_account_notification_finish_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='permission_add_new_evaluation',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('metric', 'Metric'), ('comment', 'Comment'), ('rating', 'Rating'), ('compare', 'Compare'), ('questionnaire', 'Questionnaire')], max_length=43, null=True, verbose_name='Add evaluation'),
        ),
    ]
