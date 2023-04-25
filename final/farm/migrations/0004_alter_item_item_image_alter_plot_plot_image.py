# Generated by Django 4.1.7 on 2023-04-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_alter_item_item_image_alter_plot_plot_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.ImageField(default='images/items/none.jpg', upload_to='images/items'),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_image',
            field=models.ImageField(default='images/plots/dirt.jpg', upload_to='images/plots'),
        ),
    ]