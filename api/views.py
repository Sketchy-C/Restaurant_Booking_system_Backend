from django.shortcuts import render
from rest_framework import viewsets, status, permissions, filters
from .models import MenuItem, User, UserProfile, BookingModel, HotelProfile, HotelPicture
from .serializers import MenuItemSerializer, BookingModelSerializer, UserSerializer, UserProfile, UserProfileSerializer, HotelProfile, HotelProfileSerializer, HotelPictureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ValidationError, NotFound
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found.")
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_profiles(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_profile(request, id):
    try:
        user = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        raise NotFound(detail="User not found.")
    
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def get_profile_byId(request, id):
    try:
        user = UserProfile.objects.get(user__id=id)
    except UserProfile.DoesNotExist:
        raise NotFound(detail="User not found.")
    
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_menuitems_by_hotel(request, hotel_id):
    try:
        items = MenuItem.objects.filter(hotel=hotel_id)
        if not items:
            raise NotFound(detail="No menu items found for this hotel")
    except MenuItem.DoesNotExist:
        raise NotFound(detail="Menu items not found")
    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_hotels(request):
    hotel = HotelProfile.objects.all()
    serializer = HotelProfileSerializer(hotel, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_hotel(request, id):
    try:
        hotel = HotelProfile.objects.get(user__id=id)
    except HotelProfile.DoesNotExist:
        raise NotFound(detail="Hotel not found.")
    
    serializer = HotelProfileSerializer(hotel)
    return Response(serializer.data)

class HotelProfileUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request, *args, **kwargs):
        hotel_id = kwargs.get('id') 
        try:
            hotel_profile = HotelProfile.objects.get(user__id=hotel_id)
        except HotelProfile.DoesNotExist:
            return Response({"detail": "Hotel profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HotelProfileSerializer(hotel_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def logoutt(request):
    logout(request)
    return Response({"message": "Successfully logged out"}, status=200)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"success": True, "message": "Login successful", "token": token.key,"userId": user.id })
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user_data = request.data
        if not user_data:
            return Response(
                {"error": "User data must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.create_user(**user_data)

            UserProfile.objects.create(user=user)
            if user.role == "Hotel Owner":
                HotelProfile.objects.create(user=user)
            response_data = UserSerializer(user).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class BookingUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            user_profile = BookingModel.objects.get(id=booking_id)
        except BookingModel.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingModelSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HotelProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         try:
#             hotel_profile = request.user.hotelprofile
#         except HotelProfile.DoesNotExist:
#             return Response({"detail": "Hotel profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = HotelProfileSerializer(hotel_profile)
#         return Response(serializer.data)
#     def put(self, request):
#         try:
#             hotel_profile = request.user.hotelprofile
#         except HotelProfile.DoesNotExist:
#             return Response({"detail": "Hotel profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = HotelProfileSerializer(hotel_profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HotelProfileUpdateView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def put(self, request, *args, **kwargs):
#         user_id = kwargs.get('id')
#         try:
#             user_profile = UserProfile.objects.get(user__id=user_id)
#         except UserProfile.DoesNotExist:
#             return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def bookingMade(request):
    booking = BookingModel.objects.all()
    serializer = BookingModelSerializer(booking, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_Booking_byId(request, id):
    bookings = BookingModel.objects.filter(user__id=id)

    if not bookings.exists():
        raise NotFound(detail="No bookings found for this user.")

    serializer = BookingModelSerializer(bookings, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_Booking_byHotel(request, id):
    bookings = BookingModel.objects.filter(hotel__id=id)
    if not bookings.exists():
        raise NotFound(detail="No bookings found for this user.")
    serializer = BookingModelSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_menuitems(request):
    items = MenuItem.objects.all()
    if not items:
        raise NotFound(detail="Menu not found")
    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_booking(request):
    serializer = BookingModelSerializer(data=request.data)
    if serializer.is_valid():
        hotel = serializer.validated_data.get('hotel')
        menu_item = serializer.validated_data.get('menuItem')
        if menu_item.hotel != hotel:
            return Response(
                {"error": "This menu item does not belong to the selected hotel."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"Validation Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def create_menu(request):
#     serializer = MenuItemSerializer(data=request.data)
#     if serializer.is_valid():
#         hotel = serializer.validated_data.get('hotel')
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         print(f"Validation Errors: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_menu(request):
    serializer = MenuItemSerializer(data=request.data)
    
    if serializer.is_valid():
        hotel_id = request.data.get('hotel_id')
        if hotel_id:
            hotel = HotelProfile.objects.get(id=hotel_id)
            serializer.validated_data['hotel'] = hotel

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"Validation Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_picture(request):
    serializer = HotelPictureSerializer(data=request.data)
    if serializer.is_valid():
        hotel_id = request.data.get('hotel')
        if hotel_id:
            hotel = HotelProfile.objects.get(id=hotel_id)
            serializer.validated_data['hotel'] = hotel
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"Validation Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_pictures(request):
    items = HotelPicture.objects.all()
    if not items:
        raise NotFound(detail="Menu not found")
    serializer = HotelPictureSerializer(items, many=True)
    return Response(serializer.data)


class DeletePictureView(APIView):
    def delete(self, request, pk):
        try:
            picture = HotelPicture.objects.get(id=pk)
            picture.delete()
            return Response({"message": "Picture deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except HotelPicture.DoesNotExist:
            raise NotFound(detail="Picture not found")  
        

class DeleteMenuView(APIView):
    def delete(self, request, pk):
        try:
            picture = MenuItem.objects.get(id=pk)
            picture.delete()
            return Response({"message": "Menu deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MenuItem.DoesNotExist:
            raise NotFound(detail="Menu not found")
        


