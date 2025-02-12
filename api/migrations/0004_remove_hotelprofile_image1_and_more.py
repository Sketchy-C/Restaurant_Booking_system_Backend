# Generated by Django 5.1.5 on 2025-01-27 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_role_hotelprofile_menuitem_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelprofile',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='hotelprofile',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='hotelprofile',
            name='image3',
        ),
        migrations.AlterField(
            model_name='hotelprofile',
            name='hotel_seats',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hotelprofile',
            name='no_people_per_hour',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='HotelPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(default='default.jpg', upload_to='menu_images')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_picture', to='api.hotelprofile')),
            ],
        ),
    ]
