# Generated by Django 5.1.5 on 2025-02-04 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_bookingmodel_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingmodel',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
