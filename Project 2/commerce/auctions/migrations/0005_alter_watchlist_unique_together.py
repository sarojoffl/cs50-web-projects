# Generated by Django 4.2.9 on 2024-02-10 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together=set(),
        ),
    ]
