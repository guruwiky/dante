# Generated by Django 3.2 on 2022-12-28 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20221224_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writer',
            name='balance',
            field=models.FloatField(null=True),
        ),
    ]
