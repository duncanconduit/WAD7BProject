# Generated by Django 5.1.6 on 2025-03-23 18:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_rename_location_place_address_place_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
