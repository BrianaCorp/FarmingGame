# Generated by Django 4.1.7 on 2023-04-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('item_quantity', models.IntegerField()),
                ('item_cost', models.IntegerField()),
                ('item_image', models.ImageField(default='images/items/none.jpg', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_plant', models.CharField(default='None', max_length=200)),
                ('plot_growth', models.IntegerField(default=0)),
                ('plot_watered', models.BooleanField(default=False)),
                ('plot_image', models.ImageField(default='images/plots/dirt.jpg', upload_to='images')),
            ],
        ),
    ]
