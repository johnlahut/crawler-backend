# Generated by Django 2.2.4 on 2019-08-10 17:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0003_job_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('de2ee4da-6400-439a-b82d-a3b72ad4c472'), unique=True),
        ),
    ]