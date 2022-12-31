# Generated by Django 3.2 on 2022-12-30 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_id',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
