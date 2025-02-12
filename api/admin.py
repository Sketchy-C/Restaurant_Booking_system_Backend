from django.contrib import admin
from django.contrib import admin
from .models import User, UserProfile, HotelProfile, MenuItem,HotelPicture, BookingModel

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(HotelProfile)
admin.site.register(MenuItem)
admin.site.register(HotelPicture)
admin.site.register(BookingModel)

