# Generated by Django 4.1.5 on 2023-02-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_xss_flag_1',
            field=models.BooleanField(default=False),
        ),
    ]
