# Generated by Django 4.1.2 on 2022-10-26 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_gig_deadline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gig',
            old_name='Deadline',
            new_name='deadline',
        ),
        migrations.RenameField(
            model_name='gig',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='gig',
            old_name='Price',
            new_name='price',
        ),
    ]
