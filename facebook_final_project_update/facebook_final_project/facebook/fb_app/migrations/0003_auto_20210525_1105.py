# Generated by Django 3.1.5 on 2021-05-25 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fb_app', '0002_auto_20210525_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
