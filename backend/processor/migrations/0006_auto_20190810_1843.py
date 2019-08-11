# Generated by Django 2.2.4 on 2019-08-10 18:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0005_auto_20190810_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='client_id',
            field=models.UUIDField(default=uuid.UUID('f264fa0c-b200-4eee-bcc5-ba0810cad025'), unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='task_id',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]