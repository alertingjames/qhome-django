from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    auth_status = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    stores = models.CharField(max_length=11)
    fcm_token = models.CharField(max_length=1000)

class Store(models.Model):
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    logo_url = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    category2 = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    ratings = models.CharField(max_length=11)
    reviews = models.CharField(max_length=11)
    likes = models.CharField(max_length=11)
    isLiked = models.CharField(max_length=20)
    ar_name = models.CharField(max_length=50)
    ar_category = models.CharField(max_length=100)
    ar_category2 = models.CharField(max_length=100)
    ar_description = models.CharField(max_length=2000)
    member_name = models.CharField(max_length=50)
    status2 = models.CharField(max_length=20)


class StoreLike(models.Model):
    store_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    liked_time = models.CharField(max_length=50)

class Product(models.Model):
    store_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    price = models.CharField(max_length=11)
    new_price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    likes = models.CharField(max_length=11)
    isLiked = models.CharField(max_length=20)
    ar_name = models.CharField(max_length=50)
    ar_category = models.CharField(max_length=100)
    ar_description = models.CharField(max_length=2000)
    ordereds = models.CharField(max_length=11)
    solds = models.CharField(max_length=11)
    store_name = models.CharField(max_length=50)
    ar_store_name = models.CharField(max_length=50)

class ProductPicture(models.Model):
    product_id = models.CharField(max_length=11)
    picture_url = models.CharField(max_length=1000)

class Rating(models.Model):
    store_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    member_name = models.CharField(max_length=50)
    member_photo = models.CharField(max_length=1000)
    rating = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    lang = models.CharField(max_length=10)

class ProductSave(models.Model):
    product_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=100)
    saved_time = models.CharField(max_length=50)

class CartItem(models.Model):
    imei_id = models.CharField(max_length=50)
    producer_id = models.CharField(max_length=11)
    store_id = models.CharField(max_length=11)
    store_name = models.CharField(max_length=100)
    ar_store_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=11)
    product_name = models.CharField(max_length=100)
    ar_product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    ar_category = models.CharField(max_length=100)
    price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    quantity = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=1000)


class Phone(models.Model):
    member_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Address(models.Model):
    member_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

class UsedCoupon(models.Model):
    member_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=50)
    coupon_id = models.CharField(max_length=11)
    discount = models.CharField(max_length=11)
    expire_time = models.CharField(max_length=100)
    option = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Order(models.Model):
    member_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=50)
    orderID = models.CharField(max_length=20)
    price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    shipping = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    address_line = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    discount = models.CharField(max_length=11)

class OrderItem(models.Model):
    order_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=50)
    producer_id = models.CharField(max_length=11)
    store_id = models.CharField(max_length=11)
    store_name = models.CharField(max_length=100)
    ar_store_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=11)
    product_name = models.CharField(max_length=100)
    ar_product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    ar_category = models.CharField(max_length=100)
    price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    quantity = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=1000)
    status = models.CharField(max_length=50)
    orderID = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    status2 = models.CharField(max_length=50)
    discount = models.CharField(max_length=11)
    status_time = models.CharField(max_length=50)


class Notification(models.Model):
    receiver_id = models.CharField(max_length=11)
    imei_id = models.CharField(max_length=11)
    message = models.CharField(max_length=1000)
    sender_id = models.CharField(max_length=11)
    sender_name = models.CharField(max_length=50)
    sender_email = models.CharField(max_length=80)
    sender_phone = models.CharField(max_length=1000)
    date_time = models.CharField(max_length=100)
    image_message = models.CharField(max_length=1000)


class Guest(models.Model):
    imei_id = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    address_line = models.CharField(max_length=200)
    status = models.CharField(max_length=20)


class Advertisement(models.Model):
    picture1 = models.CharField(max_length=1000)
    store1 = models.CharField(max_length=11)
    stname1 = models.CharField(max_length=100)
    picture2 = models.CharField(max_length=1000)
    store2 = models.CharField(max_length=11)
    stname2 = models.CharField(max_length=100)
    picture3 = models.CharField(max_length=1000)
    store3 = models.CharField(max_length=11)
    stname3 = models.CharField(max_length=100)

class Coupon(models.Model):
    discount = models.CharField(max_length=11)
    expire_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Winner(models.Model):
    order_id = models.CharField(max_length=11)
    won_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Info(models.Model):
    member_id = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Winner2(models.Model):
    info_id = models.CharField(max_length=11)
    won_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Account(models.Model):
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)






























