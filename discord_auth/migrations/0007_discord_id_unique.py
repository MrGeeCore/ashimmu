# Generated by Django 2.0 on 2018-01-01 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_auth', '0006_role_add_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='id',
            field=models.CharField(db_index=True, max_length=128, unique=True),
        ),
    ]
