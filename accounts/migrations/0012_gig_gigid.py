# Generated by Django 4.1.3 on 2022-11-16 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_writer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='gigID',
            field=models.CharField(max_length=200, null=True),
        ),
    ]