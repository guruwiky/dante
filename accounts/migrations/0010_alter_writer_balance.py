# Generated by Django 3.2 on 2022-12-28 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_writer_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writer',
            name='balance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
