# Generated by Django 3.2 on 2022-12-23 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_membership_subscription_usermembership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(null=True)),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.writer')),
            ],
        ),
    ]
