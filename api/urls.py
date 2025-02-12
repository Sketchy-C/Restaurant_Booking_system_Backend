from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, UserProfileUpdateView, HotelProfileUpdateView, BookingUpdateView, DeleteMenuView,DeletePictureView, get_Booking_byHotel,get_pictures, add_picture, create_menu, create_booking, get_Booking_byId, bookingMade, get_menuitems_by_hotel, get_menuitems, get_users, get_profiles, get_user, LoginView, get_hotel, get_hotels, get_profile,get_profile_byId, logoutt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('update-profile-byId/<int:id>/', UserProfileUpdateView.as_view(), name='profile-update-by-id'),
    path('update-booking-byId/<int:id>/', BookingUpdateView.as_view(), name='booking-update-by-id'),
    path('hotel/update/<int:id>/', HotelProfileUpdateView.as_view(), name='hotel-profile-update'),
    path('get-menuitemsbyid/<int:hotel_id>/', get_menuitems_by_hotel, name='get_menuitems_by_hotel'),
    path('get-users/', get_users, name='get_users'),
    path('get-bookings/', bookingMade, name='get_bookings'),
    path('get-hotels/', get_hotels, name='get_hotels'),
    path('get-menuitems/', get_menuitems, name='get_menuitems'),
    path('get-user/<int:id>/', get_user, name='get_user'),
    path('get-profile-byId/<int:id>/', get_profile_byId, name='get_profile_byId'),
    path('get-Booking-byId/<int:id>/', get_Booking_byId, name='get_Booking_byId'),
    path('get-Booking-byHotel/<int:id>/', get_Booking_byHotel, name='get_Booking_byHotel'),
    path('get-profile/<int:id>/', get_profile, name='get_profile'),
    path('get-hotel/<int:id>/', get_hotel, name='get_hotel'),
    path('get-profiles/', get_profiles, name='get_profiles'),
    path('create-booking/', create_booking, name='create_booking'),
    path('create_menu/', create_menu, name='create_menu'),
    path('add_picture/', add_picture, name='add_picture'),
    path('get_pictures/', get_pictures, name='get_pictures'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logoutt,name='logout'),
    path('delete_picture/<int:pk>/', DeletePictureView.as_view(), name='delete_picture'),
    path('delete_menu/<int:pk>/', DeleteMenuView.as_view(), name='delete_menu'),
]