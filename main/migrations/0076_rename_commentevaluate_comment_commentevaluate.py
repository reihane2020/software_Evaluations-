# Generated by Django 3.2.9 on 2021-12-27 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0075_remove_commentevaluate_commenttext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='CommentEvaluate',
            new_name='commentEvaluate',
        ),
    ]
