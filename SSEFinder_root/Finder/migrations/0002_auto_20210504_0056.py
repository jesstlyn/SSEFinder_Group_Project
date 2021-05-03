# Generated by Django 3.1.8 on 2021-05-03 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venueXCoordinates',
            field=models.DecimalField(decimal_places=10, max_digits=10, null='True'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venueYCoordinates',
            field=models.DecimalField(decimal_places=10, max_digits=10, null='True'),
        ),
    ]
