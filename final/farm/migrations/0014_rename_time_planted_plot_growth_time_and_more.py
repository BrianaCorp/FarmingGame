# Generated by Django 4.2 on 2023-04-22 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0013_plot_time_planted_plot_time_watered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plot',
            old_name='time_planted',
            new_name='growth_time',
        ),
        migrations.RenameField(
            model_name='plot',
            old_name='time_watered',
            new_name='water_time',
        ),
    ]