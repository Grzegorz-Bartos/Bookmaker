# Generated by Django 5.0.1 on 2024-10-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_coupon_potential_winnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='total_odds',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
    ]