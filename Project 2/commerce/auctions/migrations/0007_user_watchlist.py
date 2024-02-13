# Generated by Django 4.2.9 on 2024-02-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_delete_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watched_by_users', to='auctions.listing'),
        ),
    ]
