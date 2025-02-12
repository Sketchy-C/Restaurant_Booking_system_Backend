from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[
        ('user', 'User'),
        ('hotel owner', 'Hotel Owner'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    ], default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions', 
        blank=True
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300)
    image = CloudinaryField('image', default='v1738105543/pfp_birubd.jpg')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    


class HotelProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[
        ('hotel', 'Hotel'),
        ('b&b', 'Beb & Breakfast-(B&B)'),
        ('motel', 'Motel'),
        ('lodge', 'Lodge'),
        ('themed_dining_xp', 'Themed Dining XP')
    ], default='hotel')
    full_hotel_name = models.CharField(max_length=300)
    location = models.CharField(max_length=100, default=' ')
    hotel_bio = models.CharField(max_length=300)
    hotel_cover = CloudinaryField('image', default='default.jpg')
    hotel_tables = models.IntegerField(default=0)
    hotel_table_seats = models.IntegerField(default=0)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.full_hotel_name

class MenuItem(models.Model):
    hotel = models.ForeignKey(HotelProfile, on_delete=models.CASCADE, related_name='menu_items')
    type = models.CharField(max_length=50, choices=[
        ('Food', 'Food'),
        ('Beds', 'Beds'),
    ], default='Food')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image', default='default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class HotelPicture(models.Model):
    hotel = models.ForeignKey(HotelProfile, on_delete=models.CASCADE, related_name='hotel_picture')
    name = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='menu_images')
    image = CloudinaryField('image', default='default.jpg')

    def __str__(self):
        return self.name


class BookingModel(models.Model):
    hotel = models.ForeignKey(HotelProfile, on_delete=models.CASCADE, related_name='hotel_booking')
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    state = models.CharField(max_length=50, choices=[
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('rejected', 'rejected')
    ], default='pending')
    message = models.CharField(default='Pending...')
    type = models.CharField(max_length=50, choices=[
        ('Table', 'Table'),
        ('Room', 'Room')
    ], default='Table')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
