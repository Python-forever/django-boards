# Generated by Django 2.2.1 on 2019-06-18 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_usergender'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usergender',
            name='foruser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usergender', to=settings.AUTH_USER_MODEL),
        ),
    ]
