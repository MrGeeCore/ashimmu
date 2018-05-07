# Generated by Django 2.0 on 2018-05-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('discord_auth', '0007_discord_id_unique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discordrole',
            name='group',
        ),
        migrations.AddField(
            model_name='discordrole',
            name='group',
            field=models.ManyToManyField(db_index=True, related_name='discord_role', to='auth.Group'),
        ),
    ]
