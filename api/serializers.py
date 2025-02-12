from rest_framework import serializers
from .models import User, MenuItem, UserProfile, HotelProfile, HotelPicture, BookingModel

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'groups', 'user_permissions', 'password']

    def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.is_active = True
            user.save() 
            return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role == 'hotel owner':
            data['hotel_owner_info'] = 'Custom data for hotel owner'
        return data


class MenuItemSerializer(serializers.ModelSerializer):
    hotel_id = serializers.IntegerField(source='hotel.id', read_only=True)  # Add this line to return the hotel id
    
    class Meta:
        model = MenuItem
        fields = ['id', 'type', 'hotel_id', 'name', 'description', 'image', 'price']

    def get_image_url(self, obj):
        return obj.image.url



class HotelPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPicture
        fields = ['id', 'hotel', 'name', 'image']

    def get_image_url(self, obj):
        return obj.image.url 


class HotelProfileSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True) 
    hotel_picture = HotelPictureSerializer(many=True)

    class Meta:
        model = HotelProfile
        fields = ['id', 'user', 'type', 'full_hotel_name', 'location', 'hotel_bio', 'hotel_cover', 'hotel_picture','hotel_tables', 'hotel_table_seats', 'menu_items', 'email', 'phone_number']



class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'full_name', 'bio', 'image', 'verified']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError({"user": user_serializer.errors})

        return super().update(instance, validated_data)


class BookingModelSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.full_hotel_name', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    menu_item_name = serializers.CharField(source='menuItem.name', read_only=True)

    class Meta:
        model = BookingModel
        fields = ['id', 'hotel','number', 'state', 'message','hotel_name', 'menuItem', 'menu_item_name', 'user', 'user_name', 'type', 'created_at']
        read_only_fields = ['hotel_name', 'user_name', 'menu_item_name', 'created_at']
    def create(self, validated_data):
        hotel = validated_data.get('hotel')
        menu_item = validated_data.get('menuItem')
        if menu_item.hotel != hotel:
            raise serializers.ValidationError({"menuItem": "This menu item does not belong to the selected hotel."})
        return super().create(validated_data)
