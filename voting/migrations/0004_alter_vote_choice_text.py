# Generated by Django 5.0.3 on 2024-03-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_alter_vote_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='choice_text',
            field=models.CharField(choices=[('Approve', 'Approve'), ('Disapprove', 'Disapprove')], max_length=200),
        ),
    ]
