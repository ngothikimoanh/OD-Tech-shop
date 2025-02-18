# Generated by Django 5.1.4 on 2025-02-05 13:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_password_change',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
