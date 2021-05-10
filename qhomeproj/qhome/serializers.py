from rest_framework import serializers
from .models import Member, Store, StoreLike, Product, ProductPicture, Rating, ProductSave, CartItem, Phone, Address, UsedCoupon, Order, OrderItem, Notification, Advertisement, Coupon, Winner, Info, Winner2, Guest

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'password', 'phone_number', 'auth_status', 'address', 'area', 'street', 'house', 'instagram', 'registered_time', 'status', 'role', 'stores', 'fcm_token')

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'member_id', 'name', 'logo_url', 'category', 'category2', 'description', 'registered_time', 'status', 'ratings', 'reviews', 'likes', 'isLiked', 'ar_name', 'ar_category', 'ar_category2', 'ar_description', 'member_name', 'status2')

class StoreLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLike
        fields = ('id', 'store_id', 'member_id', 'liked_time')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'store_id', 'member_id', 'name', 'picture_url', 'category', 'price', 'new_price', 'unit', 'description', 'registered_time', 'status', 'likes', 'isLiked', 'ar_name', 'ar_category', 'ar_description', 'ordereds', 'solds', 'store_name', 'ar_store_name')

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = ('id', 'product_id', 'picture_url')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'store_id', 'member_id', 'member_name', 'member_photo', 'rating', 'date_time', 'subject', 'description', 'lang')

class ProductSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSave
        fields = ('id', 'product_id', 'imei_id', 'saved_time')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'imei_id', 'producer_id', 'store_id', 'store_name', 'ar_store_name', 'product_id', 'product_name', 'ar_product_name', 'category', 'ar_category', 'price', 'unit', 'quantity', 'date_time', 'picture_url')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'member_id', 'imei_id', 'phone_number', 'status')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'member_id', 'imei_id', 'address', 'area', 'street', 'house', 'status')

class UsedCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedCoupon
        fields = ('id', 'member_id', 'imei_id', 'coupon_id', 'discount', 'expire_time', 'option', 'status')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'member_id', 'imei_id', 'orderID', 'price', 'unit', 'shipping', 'date_time', 'email', 'address', 'address_line', 'phone_number', 'status', 'discount')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order_id', 'member_id', 'imei_id', 'producer_id', 'store_id', 'store_name', 'ar_store_name', 'product_id', 'product_name', 'ar_product_name', 'category', 'ar_category', 'price', 'unit', 'quantity', 'date_time', 'picture_url', 'status', 'orderID', 'contact', 'status2', 'discount', 'status_time')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'receiver_id', 'imei_id', 'message', 'sender_id', 'sender_name', 'sender_email', 'sender_phone', 'date_time', 'image_message')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'picture1', 'store1', 'stname1', 'picture2', 'store2', 'stname2', 'picture3', 'store3', 'stname3')

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'discount', 'expire_time', 'status')


class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = ('id', 'order_id', 'won_time', 'status')


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'member_id', 'date_time', 'status')


class Winner2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Winner2
        fields = ('id', 'info_id', 'won_time', 'status')


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'imei_id', 'phone_number', 'address', 'address_line', 'status')





































