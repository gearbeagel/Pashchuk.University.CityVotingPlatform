# Generated by Django 5.0.3 on 2024-04-30 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='comment_notif',
            new_name='comment_notifications',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='proposal_notif',
            new_name='proposal_notifications',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='voting_notif',
            new_name='voting_notifications',
        ),
    ]