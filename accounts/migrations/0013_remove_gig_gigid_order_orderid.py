# Generated by Django 4.1.3 on 2022-11-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_gig_gigid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gig',
            name='gigID',
        ),
        migrations.AddField(
            model_name='order',
            name='orderid',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
