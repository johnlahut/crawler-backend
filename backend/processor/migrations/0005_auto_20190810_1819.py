# Generated by Django 2.2.4 on 2019-08-10 18:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0004_auto_20190810_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='task_id',
            field=models.UUIDField(default=uuid.UUID('ffae82af-c070-4633-ac84-c8935f5da523'), unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('40140c7d-3985-45a2-9ae4-6382332c368f'), unique=True),
        ),
    ]
