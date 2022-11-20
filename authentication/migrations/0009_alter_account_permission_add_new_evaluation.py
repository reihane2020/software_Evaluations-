# Generated by Django 4.0.5 on 2022-08-02 12:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_account_permission_add_new_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='permission_add_new_evaluation',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('metric', 'Metric'), ('comment', 'Comment'), ('rating', 'Rating'), ('compare', 'Compare'), ('questionnaire', 'Questionnaire')], default=['metric'], max_length=43, null=True, verbose_name='Add evaluation'),
        ),
    ]
