import datetime
import difflib
import os
import string
import urllib
from itertools import islice

import io
import requests
import xlrd
import re

from django.core import mail
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
# from _mysql_exceptions import DataError, IntegrityError
from django.template import RequestContext

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_control
from numpy import long

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from time import gmtime, strftime
import time

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django import forms
import sys
from django.core.cache import cache
import random

from pyfcm import FCMNotification

from qhome.models import Member, Store, StoreLike, Product, ProductPicture, Rating, ProductSave, CartItem, Phone, Address, UsedCoupon, Order, OrderItem, Notification, Advertisement, Coupon, Winner, Info, Winner2, Guest, Account
from qhome.serializers import MemberSerializer, StoreSerializer, StoreLikeSerializer, ProductSerializer, ProductPictureSerializer, RatingSerializer, ProductSaveSerializer, CartItemSerializer, PhoneSerializer, AddressSerializer, UsedCouponSerializer, OrderSerializer, OrderItemSerializer, NotificationSerializer, AdvertisementSerializer, CouponSerializer, WinnerSerializer, InfoSerializer, Winner2Serializer, GuestSerializer

import pyrebase

config = {
    "apiKey": "AIzaSyD8sQq7bU0totrjzZw5FiK5lr8WQ2kjFmM",
    "authDomain": "qhome-43cdd.firebaseapp.com",
    "databaseURL": "https://qhome-43cdd.firebaseio.com",
    "storageBucket": "qhome-43cdd.appspot.com"
}

firebase = pyrebase.initialize_app(config)


def index(request):
    return HttpResponse('<h2>Hello, Qhome is working!</h2>')


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def regGuest(request):

    if request.method == 'POST':

        imei_id = request.POST.get('imei_id', '')
        guests = Guest.objects.filter(imei_id=imei_id)
        if guests.count() == 0:
            guest = Guest()
            guest.imei_id = imei_id
            guest.save()

        resp = {'result_code': '0'}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerMember(request):

    if request.method == 'POST':

        name = request.POST.get('name', '')
        imei_id = request.POST.get('imei_id', '')
        eml = request.POST.get('email', '')
        password = request.POST.get('password', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        area = request.POST.get('area', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        instagram = request.POST.get('instagram', '')
        role = request.POST.get('role', '')

        users = Member.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = Member()
            member.name = name
            member.email = eml
            member.password = password
            member.phone_number = phone_number
            member.address = address
            member.area = area
            member.street = street
            member.house = house
            member.instagram = instagram
            member.role = role
            member.registered_time = str(int(round(time.time() * 1000)))
            member.stores = '0'

            member.save()

            phone = Phone()
            phone.member_id = member.pk
            phone.phone_number = phone_number
            phone.save()

            if address != '':
                adr = Address()
                adr.member_id = member.pk
                adr.address = address
                adr.area = area
                adr.street = street
                adr.house = house
                adr.save()

            data = {
                'id': member.pk,
                'name': member.name,
                'email': member.email,
                'password': member.password,
                'address': member.address,
                'phone_number': member.phone_number,
                'area': member.area,
                'street': member.street,
                'house': member.house,
                'role': member.role,
                'instagram': member.instagram,
                'auth_status': member.auth_status,
                'registered_time': member.registered_time,
                'status': member.status,
                'stores': member.stores,
                'token': member.fcm_token
            }

            guests = Guest.objects.filter(imei_id=imei_id)
            if guests.count() > 0:
                guest = guests[0]
                guest.delete()

            resp = {'result_code': '0', 'data':data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = Member.objects.filter(email=eml, role=role)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        if password != '':
            members = Member.objects.filter(email=email, password=password, role=role)
        else:
            members = Member.objects.filter(email=email, role=role)
        resp = {}
        if members.count() > 0:
            member = members[0]
            data = {
                'id': member.pk,
                'name': member.name,
                'email': member.email,
                'password': member.password,
                'address': member.address,
                'phone_number': member.phone_number,
                'area': member.area,
                'street': member.street,
                'house': member.house,
                'role': member.role,
                'instagram': member.instagram,
                'auth_status': member.auth_status,
                'registered_time': member.registered_time,
                'status': member.status,
                'stores': member.stores,
                'token': member.fcm_token
            }

            resp = {'result_code': '0', 'data': data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = Member.objects.filter(email=email, role=role)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        members = Member.objects.filter(email=email)
        resp = {}
        if members.count() > 0:
            member = members[0]
            member.auth_status = 'verified'
            member.save()

            data = {
                'id': member.pk,
                'name': member.name,
                'email': member.email,
                'password': member.password,
                'address': member.address,
                'phone_number': member.phone_number,
                'area': member.area,
                'street': member.street,
                'house': member.house,
                'role': member.role,
                'instagram': member.instagram,
                'auth_status': member.auth_status,
                'registered_time': member.registered_time,
                'status': member.status,
                'stores': member.stores,
                'token': member.fcm_token
            }

            resp = {'result_code': '0', 'data': data}
        else:
            resp = {'result_code': '2'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerStore(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')
        category2 = request.POST.get('category2', '')
        description = request.POST.get('description', '')
        aname = request.POST.get('ar_name', '')
        acategory = request.POST.get('ar_category', '')
        acategory2 = request.POST.get('ar_category2', '')
        adescription = request.POST.get('ar_description', '')

        stores = Store.objects.filter(member_id=member_id, name=name)
        count = stores.count()

        if count == 0:
            store = Store()
            store.member_id = member_id
            store.name = name
            store.category = category
            store.category2 = category2
            store.description = description
            store.ar_name = aname
            store.ar_category = acategory
            store.ar_category2 = acategory2
            store.ar_description = adescription
            store.registered_time = str(int(round(time.time() * 1000)))
            store.ratings = '0'
            store.reviews = '0'
            store.likes = '0'

            file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_url = fs.url(filename)
            store.logo_url = settings.URL + uploaded_url

            store.save()

            stores = Store.objects.filter(member_id=member_id)

            members = Member.objects.filter(id=member_id)
            member = None
            if members.count() > 0:
                member = members[0]

            if member is not None:
                info = 'Hi, I submitted a new store info on Qhome. Please check to verify it kindly.'

                account = Account.objects.get(id=1)
                members = Member.objects.filter(email=account.email, phone_number=account.phone_number)
                admin = members[0]
                admin_id = admin.pk

                toids = []
                toids.append(admin_id)
                messageToAdmin(member_id, toids, info, 'store', store.pk)
                registerNotification(admin_id, info, member_id, member.name, member.email, member.phone_number, '')

            resp = {'result_code': '0', 'count': str(stores.count())}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStores(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '0')

        stores = Store.objects.all().order_by('-id').order_by('-id')
        if int(member_id) > 0:
            for store in stores:
                stlikes = StoreLike.objects.filter(store_id=store.pk, member_id=member_id)
                if stlikes.count() > 0:
                    store.isLiked = 'yes'
                else: store.isLiked = 'no'
        serializer = StoreSerializer(stores, many=True)

        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def likeStore(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        stlike = StoreLike()
        stlike.store_id = store_id
        stlike.member_id = member_id
        stlike.liked_time = str(int(round(time.time() * 1000)))
        stlike.save()
        stlikes = StoreLike.objects.filter(store_id=store_id)
        store = Store.objects.get(id=store_id)
        store.likes = str(stlikes.count())
        store.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unLikeStore(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        stlikes = StoreLike.objects.filter(store_id=store_id, member_id=member_id)
        if stlikes.count() > 0:
            stlike = stlikes[0]
            stlike.delete()
        stlikes = StoreLike.objects.filter(store_id=store_id)
        store = Store.objects.get(id=store_id)
        store.likes = str(stlikes.count())
        store.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def uploadProduct(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')
        price = request.POST.get('price', '')
        unit = request.POST.get('unit', '')
        description = request.POST.get('description', '')

        aname = request.POST.get('ar_name', '')
        acategory = request.POST.get('ar_category', '')
        adescription = request.POST.get('ar_description', '')

        product = Product()
        product.store_id = store_id
        product.member_id = member_id
        product.name = name
        product.category = category
        product.price = price
        product.new_price = '0'
        product.unit = unit
        product.description = description
        product.registered_time = str(int(round(time.time() * 1000)))
        product.likes = '0'
        product.ar_name = aname
        product.ar_category = acategory
        product.ar_description = adescription
        product.ordereds = '0'
        product.solds = '0'

        product.save()

        fs = FileSystemStorage()

        i = 0
        for f in request.FILES.getlist('files'):
            # print("Product File Size: " + str(f.size))
            # if f.size > 1024 * 1024 * 2:
            #     continue
            i = i + 1
            filename = fs.save(f.name, f)
            uploaded_url = fs.url(filename)
            p = ProductPicture()
            p.product_id = product.pk
            p.picture_url = settings.URL + uploaded_url
            p.save()
            if i == 1:
                product.picture_url = settings.URL + uploaded_url
                product.save()

        resp = {'result_code':'0'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updateStore(request):

    if request.method == 'POST':

        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')
        category2 = request.POST.get('category2', '')
        description = request.POST.get('description', '')

        aname = request.POST.get('ar_name', '')
        acategory = request.POST.get('ar_category', '')
        acategory2 = request.POST.get('ar_category2', '')
        adescription = request.POST.get('ar_description', '')

        store = Store.objects.get(id=store_id)
        store.member_id = member_id
        store.name = name
        store.category = category
        store.category2 = category2
        store.description = description
        store.ar_name = aname
        store.ar_category = acategory
        store.ar_category2 = acategory2
        store.ar_description = adescription
        store.status = 'updated'

        try:
            file = request.FILES['file']

            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_url = fs.url(filename)
            store.logo_url = settings.URL + uploaded_url
        except MultiValueDictKeyError:
            print('no pictures updated')

        store.save()

        stores = Store.objects.filter(member_id=member_id)

        members = Member.objects.filter(id=member_id)
        member = None
        if members.count() > 0:
            member = members[0]

        if member is not None:
            info = 'Hi, I have updated my store info on Qhome. Please check to verify it kindly.'
            account = Account.objects.get(id=1)
            members = Member.objects.filter(email=account.email, phone_number=account.phone_number)
            admin = members[0]
            admin_id = admin.pk

            toids = []
            toids.append(admin_id)
            messageToAdmin(member_id, toids, info, 'store', store.pk)
            registerNotification(admin_id, info, member_id, member.name, member.email, member.phone_number, '')

        resp = {'result_code': '0', 'count': str(stores.count())}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getProducts(request):

    if request.method == 'POST':

        imei_id = request.POST.get('imei_id', '')

        products = Product.objects.all().order_by('-id')

        for product in products:
            pss = ProductSave.objects.filter(product_id=product.pk, imei_id=imei_id)
            if pss.count() > 0:
                product.isLiked = 'yes'
            else: product.isLiked = 'no'

        serializer = ProductSerializer(products, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getRatings(request):

    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        ratings = Rating.objects.filter(store_id=store_id).order_by('-id')
        serializer = RatingSerializer(ratings, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def saveProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        imei_id = request.POST.get('imei_id', '')
        pss = ProductSave.objects.filter(product_id=product_id, imei_id=imei_id)
        if pss.count() == 0:
            ps = ProductSave()
            ps.product_id = product_id
            ps.imei_id = imei_id
            ps.saved_time = str(int(round(time.time() * 1000)))
            ps.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unsaveProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        imei_id = request.POST.get('imei_id', '')
        pss = ProductSave.objects.filter(product_id=product_id, imei_id=imei_id)
        if pss.count() > 0:
            ps = pss[0]
            ps.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getSavedProducts(request):

    if request.method == 'POST':
        imei_id = request.POST.get('imei_id', '')
        productList = []
        pss = ProductSave.objects.filter(imei_id=imei_id).order_by('-id')
        for ps in pss:
            products = Product.objects.filter(id=ps.product_id)
            if products.count() > 0:
                product = products[0]
                store = Store.objects.get(id=product.store_id)
                product.store_name = store.name
                product.ar_store_name = store.ar_name
                productList.append(product)
        serializer = ProductSerializer(productList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def placeStoreFeedback(request):

    if request.method == 'POST':

        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        subject = request.POST.get('subject', '')
        rating = request.POST.get('rating', '1')
        description = request.POST.get('description', '')
        lang = request.POST.get('lang', '')

        members = Member.objects.filter(id=member_id)
        member = None
        if members.count() > 0:
            member = members[0]
        isNew = False
        rts = Rating.objects.filter(member_id=member_id, store_id=store_id)
        if rts.count() == 0:
            rt = Rating()
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = settings.URL + '/static/qhome/images/2428675.png'
            rt.store_id = store_id
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.lang = lang
            rt.save()
            isNew = True
        else:
            rt = rts[0]
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = settings.URL + '/static/qhome/images/2428675.png'
            rt.store_id = store_id
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.lang = lang
            rt.save()

        rts = Rating.objects.filter(store_id=store_id)
        if rts.count() > 0:
            i = 0
            for rt in rts:
                if rt.rating == '':
                    rt.rating = '0'
                i = i + float(rt.rating)
            i = float(i/rts.count())
            rat = str(i)
            rat = rat[:3]
            store = Store.objects.get(id=store_id)
            store.ratings = rat
            if isNew: store.reviews = str(int(store.reviews) + 1)
            store.save()

        store = Store.objects.get(id=store_id)

        resp = {'result_code':'0', 'ratings':str(store.ratings), 'reviews':str(store.reviews), 'lang':lang}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getProductPictures(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        pps = ProductPicture.objects.filter(product_id=product_id)
        serializer = ProductPictureSerializer(pps, many=True)

        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def addToCart(request):

    if request.method == 'POST':

        imei_id = request.POST.get('imei_id', '1')
        producer_id = request.POST.get('producer_id', '1')
        store_id = request.POST.get('store_id', '1')
        store_name = request.POST.get('store_name', '')
        ar_store_name = request.POST.get('ar_store_name', '')
        product_id = request.POST.get('product_id', '1')
        product_name = request.POST.get('product_name', '')
        ar_product_name = request.POST.get('ar_product_name', '')
        category = request.POST.get('category', '')
        ar_category = request.POST.get('ar_category', '')
        price = request.POST.get('price', '0')
        unit = request.POST.get('unit', '')
        quantity = request.POST.get('quantity', '0')
        picture_url = request.POST.get('picture_url', '')

        cis = CartItem.objects.filter(imei_id=imei_id, product_id=product_id, store_id=store_id)
        count = cis.count()

        if count == 0:
            ci = CartItem()
            ci.imei_id = imei_id
            ci.producer_id = producer_id
            ci.store_id = store_id
            ci.store_name = store_name
            ci.ar_store_name = ar_store_name
            ci.product_id = product_id
            ci.product_name = product_name
            ci.ar_product_name = ar_product_name
            ci.category = category
            ci.ar_category = ar_category
            ci.price = price
            ci.unit = unit
            ci.quantity = quantity
            ci.date_time = str(int(round(time.time() * 1000)))
            ci.picture_url = picture_url

            ci.save()

        else:
            ci = cis[0]
            ci.imei_id = imei_id
            ci.producer_id = producer_id
            ci.store_id = store_id
            ci.store_name = store_name
            ci.ar_store_name = ar_store_name
            ci.product_id = product_id
            ci.product_name = product_name
            ci.ar_product_name = ar_product_name
            ci.category = category
            ci.ar_category = ar_category
            ci.price = price
            ci.unit = unit
            ci.quantity = str(int(ci.quantity) + int(quantity))
            ci.date_time = str(int(round(time.time() * 1000)))
            ci.picture_url = picture_url

            ci.save()

        resp = {'result_code': '0'}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getCartItems(request):

    if request.method == 'POST':
        imei_id = request.POST.get('imei_id', '1')
        cis = CartItem.objects.filter(imei_id=imei_id).order_by('-id')
        serializer = CartItemSerializer(cis, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delCartItem(request):

    if request.method == 'POST':
        item_id = request.POST.get('item_id', '1')
        item = CartItem.objects.get(id=item_id)
        if item is not None:
            item.delete()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updateCartItemQuantity(request):

    if request.method == 'POST':
        item_id = request.POST.get('item_id', '1')
        quantity = request.POST.get('quantity', '1')
        item = CartItem.objects.get(id=item_id)
        if item is not None:
            item.quantity = quantity
            item.save()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def addCartToWishlist(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id', '1')
        imei_id = request.POST.get('imei_id', '')
        item = CartItem.objects.get(id=item_id)
        product_id = item.product_id
        pss = ProductSave.objects.filter(product_id=product_id, imei_id=imei_id)
        if pss.count() == 0:
            ps = ProductSave()
            ps.product_id = product_id
            ps.imei_id = imei_id
            ps.saved_time = str(int(round(time.time() * 1000)))
            ps.save()
        item.delete()

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def productInfo(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        imei_id = request.POST.get('imei_id', '')
        product = Product.objects.get(id=product_id)

        pss = ProductSave.objects.filter(product_id=product.pk, imei_id=imei_id)
        if pss.count() > 0:
            product.isLiked = 'yes'
        else: product.isLiked = 'no'

        stores = Store.objects.filter(id=product.store_id)
        store = None
        if stores.count() > 0:
            store = stores[0]
        if store is not None:
            product.store_name = store.name
            product.ar_store_name = store.ar_name

        data={
            'id':product.id,
            'store_id':product.store_id,
            'member_id':product.member_id,
            'name':product.name,
            'picture_url':product.picture_url,
            'category':product.category,
            'price':product.price,
            'new_price':product.new_price,
            'unit':product.unit,
            'description':product.description,
            'registered_time':product.registered_time,
            'status':product.status,
            'likes':product.likes,
            'isLiked':product.isLiked,
            'ar_name':product.ar_name,
            'ar_category':product.ar_category,
            'ar_description':product.ar_description,
            'ordereds':product.ordereds,
            'solds':product.solds,
            'store_name':product.store_name,
            'ar_store_name':product.ar_store_name
        }

        resp = {'result_code':'0', 'data':data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def addWishlistToCart(request):

    if request.method == 'POST':

        imei_id = request.POST.get('imei_id', '1')
        producer_id = request.POST.get('producer_id', '1')
        store_id = request.POST.get('store_id', '1')
        store_name = request.POST.get('store_name', '')
        ar_store_name = request.POST.get('ar_store_name', '')
        product_id = request.POST.get('product_id', '1')
        product_name = request.POST.get('product_name', '')
        ar_product_name = request.POST.get('ar_product_name', '')
        category = request.POST.get('category', '')
        ar_category = request.POST.get('ar_category', '')
        price = request.POST.get('price', '0')
        unit = request.POST.get('unit', '')
        quantity = request.POST.get('quantity', '0')
        picture_url = request.POST.get('picture_url', '')

        cis = CartItem.objects.filter(imei_id=imei_id, product_id=product_id, store_id=store_id)
        count = cis.count()

        if count == 0:
            ci = CartItem()
            ci.imei_id = imei_id
            ci.producer_id = producer_id
            ci.store_id = store_id
            ci.store_name = store_name
            ci.ar_store_name = ar_store_name
            ci.product_id = product_id
            ci.product_name = product_name
            ci.ar_product_name = ar_product_name
            ci.category = category
            ci.ar_category = ar_category
            ci.price = price
            ci.unit = unit
            ci.quantity = quantity
            ci.date_time = str(int(round(time.time() * 1000)))
            ci.picture_url = picture_url

            ci.save()

        else:
            ci = cis[0]
            ci.imei_id = imei_id
            ci.producer_id = producer_id
            ci.store_id = store_id
            ci.store_name = store_name
            ci.ar_store_name = ar_store_name
            ci.product_id = product_id
            ci.product_name = product_name
            ci.ar_product_name = ar_product_name
            ci.category = category
            ci.ar_category = ar_category
            ci.price = price
            ci.unit = unit
            ci.quantity = str(int(ci.quantity) + int(quantity))
            ci.date_time = str(int(round(time.time() * 1000)))
            ci.picture_url = picture_url

            ci.save()

        pss = ProductSave.objects.filter(product_id=product_id, imei_id=imei_id)
        if pss.count() > 0:
            ps = pss[0]
            ps.delete()

        resp = {'result_code': '0'}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getPhones(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        imei_id = request.POST.get('imei_id', '1')

        pns = Phone.objects.filter(imei_id=imei_id).order_by('-id')
        phoneList = []
        for pn in pns: phoneList.append(pn)
        if int(member_id) > 0:
            pns2 = Phone.objects.filter(member_id=member_id).order_by('-id')
            for pn in pns2:
                if pn not in phoneList: phoneList.append(pn)
        serializer = PhoneSerializer(phoneList, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getAddresses(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        imei_id = request.POST.get('imei_id', '1')

        ads = Address.objects.filter(imei_id=imei_id).order_by('-id')
        addrList = []
        for ad in ads: addrList.append(ad)
        if int(member_id) > 0:
            ads2 = Address.objects.filter(member_id=member_id).order_by('-id')
            for ad in ads2:
                if ad not in addrList: addrList.append(ad)
        serializer = AddressSerializer(addrList, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def savePhoneNumber(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        imei_id = request.POST.get('imei_id', '1')
        phone_number = request.POST.get('phone_number', '')

        if int(member_id) > 0:
            phones = Phone.objects.filter(member_id=member_id, phone_number=phone_number)
            if phones.count() == 0:
                phone = Phone()
                phone.member_id = member_id
                phone.imei_id = imei_id
                phone.phone_number = phone_number
                phone.save()
                resp = {'result_code':'0'}
            else: resp = {'result_code':'1'}
        else:
            phones = Phone.objects.filter(imei_id=imei_id, phone_number=phone_number)
            if phones.count() == 0:
                phone = Phone()
                phone.member_id = member_id
                phone.imei_id = imei_id
                phone.phone_number = phone_number
                phone.save()
                resp = {'result_code':'0'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def saveAddress(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        imei_id = request.POST.get('imei_id', '1')
        address = request.POST.get('address', '')
        area = request.POST.get('area', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')

        if int(member_id) > 0:
            adrs = Address.objects.filter(member_id=member_id, address=address, area=area, street=street, house=house)
            if adrs.count() == 0:
                adr = Address()
                adr.member_id = member_id
                adr.imei_id = imei_id
                adr.address = address
                adr.area = area
                adr.street = street
                adr.house = house
                adr.save()
                resp = {'result_code':'0'}
            else: resp = {'result_code':'1'}
        else:
            adrs = Address.objects.filter(imei_id=imei_id, address=address, area=area, street=street, house=house)
            if adrs.count() == 0:
                adr = Address()
                adr.member_id = member_id
                adr.imei_id = imei_id
                adr.address = address
                adr.area = area
                adr.street = street
                adr.house = house
                adr.save()
                resp = {'result_code':'0'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delAddress(request):

    if request.method == 'POST':
        addr_id = request.POST.get('addr_id', '1')
        addr = Address.objects.get(id=addr_id)
        if addr is not None:
            addr.delete()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delPhone(request):

    if request.method == 'POST':
        phone_id = request.POST.get('phone_id', '1')
        phone = Phone.objects.get(id=phone_id)
        if phone is not None:
            phone.delete()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def uploadOrder(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '0')
        imei_id = request.POST.get('imei_id', '')
        orderID = request.POST.get('orderID', '')
        price = request.POST.get('price', '0')
        unit = request.POST.get('unit', '')
        shipping = request.POST.get('shipping', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        address_line = request.POST.get('address_line', '')
        phone_number = request.POST.get('phone_number', '')
        coupon_id = request.POST.get('coupon_id', '0')
        discount = request.POST.get('discount', '0')

        orderItems = request.POST.get('orderItems', '')

        order = Order()
        order.member_id = member_id
        order.imei_id = imei_id
        order.orderID = orderID
        order.price = price
        order.unit = unit
        order.shipping = shipping
        order.date_time = str(int(round(time.time() * 1000)))
        order.email = email
        order.address = address
        order.address_line = address_line
        order.phone_number = phone_number
        order.status = 'placed'
        order.discount = discount

        order.save()

        if int(member_id) == 0:
            guests = Guest.objects.filter(imei_id=imei_id)
            guest = guests[0]
            guest.phone_number = phone_number
            guest.address = address
            guest.address_line = address_line
            guest.save()

        try:
            decoded = json.loads(orderItems)
            for orderItem_data in decoded['orderItems']:

                member_id = orderItem_data['member_id']
                producer_id = orderItem_data['producer_id']
                imei_id = orderItem_data['imei_id']
                store_id = orderItem_data['store_id']
                store_name = orderItem_data['store_name']
                ar_store_name = orderItem_data['ar_store_name']
                product_id = orderItem_data['product_id']
                product_name = orderItem_data['product_name']
                ar_product_name = orderItem_data['ar_product_name']
                category = orderItem_data['category']
                ar_category = orderItem_data['ar_category']
                price = orderItem_data['price']
                unit = orderItem_data['unit']
                quantity = orderItem_data['quantity']
                date_time = order.date_time
                picture_url = orderItem_data['picture_url']

                item = OrderItem()
                item.order_id = order.pk
                item.member_id = member_id
                item.imei_id = imei_id
                item.producer_id = producer_id
                item.store_id = store_id
                item.store_name = store_name
                item.ar_store_name = ar_store_name
                item.product_id = product_id
                item.product_name = product_name
                item.ar_product_name = ar_product_name
                item.category = category
                item.ar_category = ar_category
                item.price = price
                item.unit = unit
                item.quantity = quantity
                item.date_time = date_time
                item.picture_url = picture_url
                item.status = 'placed'
                item.discount = order.discount
                item.status_time = date_time

                item.save()

                itemInfo = 'Order ID: ' + orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n' + 'Order Status: Order Placed' + '\n' + 'Item Name: ' + item.product_name + ' ' + item.ar_product_name + '\n' + 'Item Category: ' + item.category + ' ' + item.ar_category + '\n' + 'Item Price: ' + item.price + ' QR' + '\n' + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name + ' ' + item.ar_store_name

                if int(member_id) > 0:
                    member = Member.objects.get(id=member_id)
                    info = 'Hi, I placed a new order on Qhome.\n' + itemInfo + '\nPlease check to process it kindly.'
                    toids = []
                    toids.append(producer_id)
                    sendMessage(member_id, toids, info, 'order')
                    registerNotification(producer_id, info, member_id, member.name, member.email, member.phone_number, '')
                else:
                    info = 'Hi, I placed a new order on Qhome.\n' + itemInfo + '\nPlease check to process it kindly.'
                    toids = []
                    toids.append(producer_id)
                    sendMessage(member_id, toids, info, 'order')
                    registerNotification(producer_id, info, member_id, 'Qhome Customer', '', phone_number, '')

                sendFCMPushNotification(producer_id, member_id, info)

            if int(coupon_id) > 0:
                ucoupon = UsedCoupon()
                ucoupon.member_id = member_id
                ucoupon.imei_id = imei_id
                ucoupon.coupon_id = coupon_id
                ucoupon.discount = discount
                coupon = Coupon.objects.get(id=coupon_id)
                ucoupon.expire_time = coupon.expire_time
                ucoupon.status = 'used'
                ucoupon.save()

            resp = {'result_code': '0', 'orderID':order.orderID, 'date_time':order.date_time}
            return HttpResponse(json.dumps(resp))

        except:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))


def orderData(orders):
    orderList = []
    for order in orders:
        member_name = ''
        if int(order.member_id) > 0:
            members = Member.objects.filter(id=order.member_id)
            if members.count() > 0:
                member = members[0]
                member_name = member.name
        won = 'no'
        winners = Winner.objects.filter(order_id=order.pk)
        if winners.count() > 0:
            won = 'yes'
        items = OrderItem.objects.filter(order_id=order.pk)
        for item in items:
            producers = Member.objects.filter(id=item.producer_id)
            if producers.count() > 0:
                producer = producers[0]
                item.contact = producer.phone_number
        serializer = OrderItemSerializer(items, many=True)

        data = {
            'id':order.pk,
            'member_id':order.member_id,
            'imei_id':order.imei_id,
            'orderID':order.orderID,
            'price':order.price,
            'unit':order.unit,
            'shipping':order.shipping,
            'date_time':order.date_time,
            'email':order.email,
            'address':order.address,
            'address_line':order.address_line,
            'phone_number':order.phone_number,
            'status':order.status,
            'discount':order.discount,
            'items':serializer.data,
            'member_name':member_name,
            'won':won,
        }

        orderList.append(data)
    return orderList


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getUserOrders(request):
    if request.method == 'POST':
        me_id = request.POST.get('me_id', '1')
        orderList = []
        orders = Order.objects.filter(member_id=me_id).order_by('-id')
        for order in orders:
            orderList.append(order)

        resp = {'result_code':'0', 'data':orderData(orderList)}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delOrder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '1')
        order = Order.objects.get(id=order_id)
        if order is not None:
            items = OrderItem.objects.filter(order_id=order.pk)
            for item in items:
                item.delete()
            order.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def userOrderItems(request):
    if request.method == 'POST':
        me_id = request.POST.get('me_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(member_id=me_id).order_by('-id')
        for item in items:
            orders = Order.objects.filter(id=item.order_id)
            order = None
            if orders.count() > 0:
                order = orders[0]
            if order is not None:
                item.orderID = order.orderID
                producers = Member.objects.filter(id=item.producer_id)
                producer = None
                if producers.count() > 0:
                    producer = producers[0]
                    item.contact = producer.phone_number
                    itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updateMember(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        area = request.POST.get('area', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        instagram = request.POST.get('instagram', '')

        member = Member.objects.get(id=member_id)

        if member is not None:
            member.name = name
            member.email = eml
            member.phone_number = phone_number
            member.address = address
            member.area = area
            member.street = street
            member.house = house
            member.instagram = instagram

            member.save()

            data = {
                'id': member.pk,
                'name': member.name,
                'email': member.email,
                'password': member.password,
                'address': member.address,
                'phone_number': member.phone_number,
                'area': member.area,
                'street': member.street,
                'house': member.house,
                'role': member.role,
                'instagram': member.instagram,
                'auth_status': member.auth_status,
                'registered_time': member.registered_time,
                'status': member.status,
                'stores': member.stores,
                'token': member.fcm_token
            }

            resp = {'result_code': '0', 'data':data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def receivedOrderItems(request):
    if request.method == 'POST':
        me_id = request.POST.get('me_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(producer_id=me_id).order_by('-id')
        for item in items:
            if item.status2 != 'canceled':
                orders = Order.objects.filter(id=item.order_id)
                if orders.count() > 0:
                    order = orders[0]
                    item.orderID = order.orderID
                    item.contact = order.phone_number
                    itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def cancelOrderItem(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id', '1')
        item = OrderItem.objects.get(id=item_id)
        if item is not None:
            item.status2 = 'canceled'
            item.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def progressOrderItem(request):
    if request.method == 'POST':
        me_id = request.POST.get('me_id', '1')
        item_id = request.POST.get('item_id', '1')
        next = request.POST.get('next', '')
        item = OrderItem.objects.get(id=item_id)
        if item is not None:
            item.status = next
            item.status_time = str(int(round(time.time() * 1000)))
            item.save()

            me = Member.objects.get(id=me_id)

            orders = Order.objects.filter(id=item.order_id)
            if orders.count() > 0:
                order = orders[0]
                status = item.status
                if item.status == 'confirmed':status = 'Order Confirmed'
                elif item.status == 'prepared':status = 'Order Prepared'
                elif item.status == 'ready':status = 'Order Ready'
                elif item.status == 'delivered':status = 'Order Delivered'
                itemInfo = 'Order ID: ' + order.orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n' + 'Order Status: ' + status + '\n' + 'Item Name: ' + item.product_name + ' ' + item.ar_product_name + '\n' + 'Item Category: ' + item.category + ' ' + item.ar_category + '\n' + 'Item Price: ' + item.price + ' QR' + '\n' + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name + ' ' + item.ar_store_name
                info = 'Hi, I upgraded your order on Qhome.\n' + itemInfo + '\nPlease check.'
                if int(item.member_id) > 0:
                    toids = []
                    toids.append(item.member_id)
                    sendMessage(me_id, toids, info, 'order_upgrade')
                    registerNotification(item.member_id, info, me_id, me.name, me.email, me.phone_number, '')

                    sendFCMPushNotification(item.member_id, me_id, info)

                itemsList = []
                items = OrderItem.objects.filter(producer_id=me_id).order_by('-id')
                for item in items:
                    if item.status2 != 'canceled':
                        orders = Order.objects.filter(id=item.order_id)
                        if orders.count() > 0:
                            order = orders[0]
                            item.orderID = order.orderID
                            item.contact = order.phone_number
                            itemsList.append(item)
                serializer = OrderItemSerializer(itemsList, many=True)

                resp = {'result_code':'0', 'next':next, 'data':serializer.data}
                return HttpResponse(json.dumps(resp))
            else:
                resp = {'result_code':'1'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def orderById(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '1')
        order = Order.objects.get(id=order_id)

        items = OrderItem.objects.filter(order_id=order.pk)
        for item in items:
            producers = Member.objects.filter(id=item.producer_id)
            if producers.count() > 0:
                producer = producers[0]
                item.contact = producer.phone_number
        serializer = OrderItemSerializer(items, many=True)

        data = {
            'id':order.pk,
            'member_id':order.member_id,
            'imei_id':order.imei_id,
            'orderID':order.orderID,
            'price':order.price,
            'unit':order.unit,
            'shipping':order.shipping,
            'date_time':order.date_time,
            'email':order.email,
            'address':order.address,
            'address_line':order.address_line,
            'phone_number':order.phone_number,
            'status':order.status,
            'discount':order.discount,
            'items':serializer.data,
        }

        resp = {'result_code':'0', 'data':data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def favoriteStores(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '')
        storeList = []
        sls = StoreLike.objects.filter(member_id=member_id).order_by('-id')
        for sl in sls:
            stores = Store.objects.filter(id=sl.store_id)
            if stores.count() > 0:
                store = stores[0]
                storeList.append(store)
        serializer = StoreSerializer(storeList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def placeAppFeedback(request):

    if request.method == 'POST':

        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        subject = request.POST.get('subject', '')
        rating = request.POST.get('rating', '1')
        description = request.POST.get('description', '')
        lang = request.POST.get('lang', '')

        member = Member.objects.get(id=member_id)
        rts = Rating.objects.filter(member_id=member_id, store_id=store_id)
        if rts.count() == 0:
            rt = Rating()
            rt.member_id = member_id
            rt.member_name = member.name
            rt.member_photo = settings.URL + '/static/qhome/images/2428675.png'
            rt.store_id = store_id
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.lang = lang
            rt.save()
        else:
            rt = rts[0]
            rt.member_id = member_id
            rt.member_name = member.name
            rt.member_photo = settings.URL + '/static/qhome/images/2428675.png'
            rt.store_id = store_id
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.lang = lang
            rt.save()

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


def sendMessage(fromid, toids, message, opt):
    fromemail = ''
    fromname = ''
    if int(fromid) > 0:
        fromMembers = Member.objects.filter(id=fromid)
        if fromMembers.count() > 0:
            fromMember = fromMembers[0]
            fromemail = fromMember.email
            fromname = fromMember.name
        else:
            fromemail = 'qhomenewuser@email.com'
            fromname = 'Qhome New User'
    else:
        fromemail = 'qhomenewuser@email.com'
        fromname = 'Qhome New User'

    db = firebase.database()

    data = {
        "msg": message,
        "date":str(int(round(time.time() * 1000))),
        "fromid": str(fromid),
        "fromname": fromname
    }

    toEmailList = []
    for toid in toids:
        toMembers = Member.objects.filter(id=toid)
        if toMembers.count() > 0:
            toMember = toMembers[0]
            toEmailList.append(toMember.email)
            if opt == 'order':
                db.child("order").child(str(toMember.pk)).push(data)
            elif opt == 'admin':
                db.child("admin").child(str(toMember.pk)).push(data)
            elif opt == 'order_upgrade':
                db.child("order_upgrade").child(str(toMember.pk)).push(data)

    subject = 'Qhome Transaction'
    if opt == 'admin': subject = 'Qhome Admin'
    elif opt == 'order':
        subject = 'Qhome New Order Information'
        message = message + '\n' + fromname
    elif opt == 'order_upgrade':
        subject = 'Qhome Order Upgrade Information'
        message = message + '\n' + fromname

    # msg = EmailMultiAlternatives(subject, message, fromemail, toEmailList)
    # msg.send(fail_silently=False)


def messageToAdmin(fromid, toids, message, type, id):
    fromemail = ''
    fromname = ''
    fromMember = None
    if int(fromid) > 0:
        fromMembers = Member.objects.filter(id=fromid)
        if fromMembers.count() > 0:
            fromMember = fromMembers[0]
            fromemail = fromMember.email
            fromname = fromMember.name
        else:
            fromemail = 'qhomenewuser@email.com'
            fromname = 'Qhome New User'
    else:
        fromemail = 'qhomenewuser@email.com'
        fromname = 'Qhome New User'
    db = firebase.database()

    data = {
        "msg": message,
        "date":str(int(round(time.time() * 1000))),
        "fromid": str(fromid),
        "fromname": fromname,
        "type":type,
        "id":id
    }

    toEmailList = []
    for toid in toids:
        toMembers = Member.objects.filter(id=toid)
        if toMembers.count() > 0:
            toMember = toMembers[0]
            toEmailList.append(toMember.email)
            if fromMember is not None:
                db.child("toadmin").child(str(fromMember.pk)).push(data)

    subject = 'Qhome Transaction'
    if type == 'store': subject = 'Qhome Store Information'
    message = message + '\nRegards\n' + fromname
    # msg = EmailMultiAlternatives(subject, message, fromemail, toEmailList)
    # msg.send(fail_silently=False)


def sendAdminMessage(fromid, toids, message, image):

    fromMembers = Member.objects.filter(id=fromid)
    if fromMembers.count() > 0:
        fromMember = fromMembers[0]
        fromemail = fromMember.email
        fromname = fromMember.name
        fromphone = fromMember.phone_number

    db = firebase.database()

    data = {
        "msg": message,
        "img": image,
        "date":str(int(round(time.time() * 1000))),
        "fromid": str(fromid),
        "fromname": fromname
    }

    toEmailList = []
    for toid in toids:
        toMembers = Member.objects.filter(id=toid)
        if toMembers.count() > 0:
            toMember = toMembers[0]
            toEmailList.append(toMember.email)
            db.child("admin").child(str(toMember.pk)).push(data)
            sendAdminNotification(toid, '', message, fromid, image)

    subject = 'Qhome Admin'

    # msg = EmailMultiAlternatives(subject, message, fromemail, toEmailList)
    # msg.send(fail_silently=False)



def adminBroadcast(fromid, toids, message, image):

    fromMembers = Member.objects.filter(id=fromid)
    if fromMembers.count() > 0:
        fromMember = fromMembers[0]
        fromemail = fromMember.email
        fromname = fromMember.name
        fromphone = fromMember.phone_number

    db = firebase.database()

    data = {
        "msg": message,
        "img": image,
        "date":str(int(round(time.time() * 1000))),
        "fromid": str(fromid),
        "fromname": fromname
    }

    toEmailList = []
    for toid in toids:
        toMembers = Member.objects.filter(id=toid)
        if toMembers.count() > 0:
            toMember = toMembers[0]
            toEmailList.append(toMember.email)
            db.child("admin").child(str(toMember.pk)).push(data)
            sendAdminNotification(toid, '', message, fromid, image)

            sendFCMPushNotification(toid, fromid, message)

    guests = Guest.objects.all()
    for guest in guests:
        db.child("admin").child(str(guest.imei_id)).push(data)
        sendAdminNotification('0', guest.imei_id, message, fromid, image)

    #    sendFCMPushNotification('0', fromid, message)

    subject = 'Qhome Admin'

    # msg = EmailMultiAlternatives(subject, message, fromemail, toEmailList)
    # msg.send(fail_silently=False)



def sendAdminNotification(receiverid, imeid, message, senderid, image):
    senders = Member.objects.filter(id=senderid)
    if senders.count() > 0:
        sender = senders[0]
        noti = Notification()
        noti.receiver_id = receiverid
        noti.imei_id = imeid
        noti.message = message
        noti.sender_id = sender.pk
        noti.sender_name = 'Qhome'
        noti.sender_email = sender.email
        noti.sender_phone = sender.phone_number
        noti.date_time = str(int(round(time.time() * 1000)))
        noti.image_message = image
        noti.save()



#inserting the token into database, after receiving it from Volley
@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def fcm_insert(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', 1)
        token = request.POST.get('fcm_token', '')
        member = Member.objects.get(id=member_id)
        member.fcm_token = token
        member.save()
        resp = {'result_code':'0', 'fcm_token':token}
        return JsonResponse(resp)

def sendFCMPushNotification(member_id, sender_id, notiText):
    date_time = str(time.strftime('%d/%m/%Y %H:%M'))
    members = Member.objects.filter(id=member_id)
    if members.count() > 0:
        member = members[0]
        message_title = 'Qhome User'
        if int(sender_id) > 0:
            senders = Member.objects.filter(id=sender_id)
            if senders.count() > 0:
                sender = senders[0]
                message_title = sender.name
        path_to_fcm = "https://fcm.googleapis.com"
        server_key = settings.FCM_LEGACY_SERVER_KEY
        reg_id = member.fcm_token #quick and dirty way to get that ONE fcmId from table
        if reg_id != '':
            message_body = notiText
            result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body, sound = 'ping.aiff', badge = 1)


def registerNotification(receiverid, message, senderid, sendername, senderemail, senderphone, image):
    if int(senderid) > 0:
        senders = Member.objects.filter(id=senderid)
        if senders.count() > 0:
            sender = senders[0]
            noti = Notification()
            noti.receiver_id = receiverid
            noti.message = message
            noti.sender_id = sender.pk
            noti.sender_name = sender.name
            noti.sender_email = sender.email
            noti.sender_phone = sender.phone_number
            noti.date_time = str(int(round(time.time() * 1000)))
            noti.image_message = image
            noti.save()
    else:
        noti = Notification()
        noti.receiver_id = receiverid
        noti.message = message
        noti.sender_id = senderid
        noti.sender_name = sendername
        noti.sender_email = senderemail
        noti.sender_phone = senderphone
        noti.date_time = str(int(round(time.time() * 1000)))
        noti.image_message = image
        noti.save()

    resp = {'result_code':'0'}
    return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getNotifications(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id', '1')
        notifications = Notification.objects.filter(receiver_id=receiver_id).order_by('-id')
        serializer = NotificationSerializer(notifications, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forGuestNotifications(request):
    if request.method == 'POST':
        imei_id = request.POST.get('imei_id', '')
        notifications = Notification.objects.filter(imei_id=imei_id).order_by('-id')
        serializer = NotificationSerializer(notifications, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delNotification(request):
    if request.method == 'POST':
        noti_id = request.POST.get('notification_id', '1')
        noti = Notification.objects.get(id=noti_id)
        noti.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        message = 'You are allowed to reset your password from your request.<br>For it, please click this link to reset your password.<br><br>https://qhome.pythonanywhere.com/resetpassword?email=' + email

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="https://qhome.pythonanywhere.com/"><img src="https://qhome.pythonanywhere.com/static/qhome/images/qlogo.png" style="width:150px;height:150px;border-radius: 8%; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">Qhome User's Security Update Information</h2>
                            <div style="font-size:16px; word-break: break-all; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = 'qhome974@gmail.com'
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))


def resetpassword(request):
    email = request.GET['email']
    return render(request, 'qhome/resetpwd.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if len(password) < 8:
            return render(request, 'qhome/result.html',
                          {'response': 'Please enter password of characters more than 8.'})
        if password != repassword:
            return render(request, 'qhome/result.html',
                          {'response': 'Please enter the same password.'})
        members = Member.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'qhome/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'qhome/result.html',
                          {'response': 'You haven\'t been registered.'})
    else: pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getAds(request):
    if request.method == 'POST':
        ads = Advertisement.objects.filter(id=1)
        resp = {}
        if ads.count() > 0:
            ad = ads[0]
            data = {
                'adPic1': ad.picture1,
                'adStore1': ad.store1,
                'adPic2': ad.picture2,
                'adStore2': ad.store2,
                'adPic3': ad.picture3,
                'adStore3': ad.store3,
            }

            resp = {'result_code':'0', 'data':data}
        else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getCoupons(request):
    if request.method == 'POST':
        me_id = request.POST.get('me_id','1')
        availableList = []
        expiredList = []
        usedList = []

        # useds = UsedCoupon.objects.filter(member_id=me_id).order_by('-id')
        # for used in useds:
        #     coupon = Coupon()
        #     coupon.id = int(used.coupon_id)
        #     coupon.discount = used.discount
        #     coupon.expire_time = used.expire_time
        #     usedList.append(coupon)

        coupons = Coupon.objects.all().order_by('-id')
        for coupon in coupons:
            current = int(round(time.time() * 1000))
            if current > int(coupon.expire_time):
                expiredList.append(coupon)
            useds = UsedCoupon.objects.filter(coupon_id=coupon.pk, member_id=me_id)
            if useds.count() > 0:
                usedList.append(coupon)
            if coupon not in expiredList and coupon not in usedList:
                availableList.append(coupon)

        serializer_expired = CouponSerializer(expiredList, many=True)
        serializer_used = CouponSerializer(usedList, many=True)
        serializer_available = CouponSerializer(availableList, many=True)

        resp = {'result_code':'0', 'expireds':serializer_expired.data, 'useds':serializer_used.data, 'availables':serializer_available.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def contactAdmin(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id','1')
        message = request.POST.get('message','')
        type = request.POST.get('type','')

        account = Account.objects.get(id=1)
        members = Member.objects.filter(email=account.email, phone_number=account.phone_number)
        admin = members[0]
        admin_id = admin.pk

        toids = []
        toids.append(admin_id)
        messageToAdmin(member_id, toids, message, type, member_id)
        members = Member.objects.filter(id=member_id)
        if members.count() > 0:
            member = members[0]
            registerNotification(admin_id, message, member_id, member.name, member.email, member.phone_number, '')

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def postLuckyInfo(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')

        now = int(round(time.time()))
        date = datetime.datetime.fromtimestamp(now)
        nowDay = date.day
        nowMonth = date.month
        nowYear = date.year

        infos = Info.objects.all()

        isExistsWinner = False

        for info in infos:
            info_date = datetime.datetime.fromtimestamp(int(int(info.date_time)/1000))
            day = info_date.day
            month = info_date.month
            year = info_date.year
            if day == nowDay and month == nowMonth and year == nowYear:
                if info.status == 'won':
                    if int(info.member_id) != int(member_id):
                        members = Member.objects.filter(id=info.member_id)
                        if members.count() > 0:
                            member = members[0]
                            data = {
                                'id': info.pk,
                                'member_id': info.member_id,
                                'member_name': member.name,
                                'date_time': info.date_time,
                                'status': info.status,
                            }

                            isExistsWinner = True
                            resp = {'result_code':'1', 'data':data}
                        break

        if isExistsWinner == False:
            info = Info()
            info.member_id = member_id
            info.date_time = str(int(round(time.time() * 1000)))
            info.save()
            resp = {'result_code':'0'}

        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getMyLuckyInfo(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')

        now = int(round(time.time()))
        date = datetime.datetime.fromtimestamp(now)
        nowDay = date.day
        nowMonth = date.month
        nowYear = date.year
        infos = Info.objects.all()

        resp = {'result_code':'0'}

        for info in infos:
            info_date = datetime.datetime.fromtimestamp(int(int(info.date_time)/1000))
            day = info_date.day
            month = info_date.month
            year = info_date.year
            if day == nowDay and month == nowMonth and year == nowYear:
                if int(info.member_id) == int(member_id):
                    members = Member.objects.filter(id=info.member_id)
                    if members.count() > 0:
                        member = members[0]
                        data = {
                            'id': info.pk,
                            'member_id': info.member_id,
                            'member_name': member.name,
                            'date_time': info.date_time,
                            'status': info.status,
                        }

                        resp = {'result_code':'1', 'data':data}
                    break;
                else:
                    if info.status == 'won':
                        members = Member.objects.filter(id=info.member_id)
                        if members.count() > 0:
                            member = members[0]
                            data = {
                                'id': info.pk,
                                'member_id': info.member_id,
                                'member_name': member.name,
                                'date_time': info.date_time,
                                'status': info.status,
                            }

                            resp = {'result_code':'2', 'data':data}
                        break;

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def uploadProduct2(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')
        price = request.POST.get('price', '')
        unit = request.POST.get('unit', '')
        description = request.POST.get('description', '')

        aname = request.POST.get('ar_name', '')
        acategory = request.POST.get('ar_category', '')
        adescription = request.POST.get('ar_description', '')

        product = Product()
        product.store_id = store_id
        product.member_id = member_id
        product.name = name
        product.category = category
        product.price = price
        product.new_price = '0'
        product.unit = unit
        product.description = description
        product.registered_time = str(int(round(time.time() * 1000)))
        product.likes = '0'
        product.ar_name = aname
        product.ar_category = acategory
        product.ar_description = adescription
        product.ordereds = '0'
        product.solds = '0'

        product.save()

        fs = FileSystemStorage()

        cnt = request.POST.get('pic_count', '1')

        for i in range(0, int(cnt)):
            f  = request.FILES["file" + str(i)]

            # print("Product File Size: " + str(f.size))
            # if f.size > 1024 * 1024 * 2:
            #     continue

            filename = fs.save(f.name, f)
            uploaded_url = fs.url(filename)
            p = ProductPicture()
            p.product_id = product.pk
            p.picture_url = settings.URL + uploaded_url
            p.save()
            if i == 0:
                product.picture_url = settings.URL + uploaded_url
                product.save()

        resp = {'result_code':'0'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def checkmember(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        member = Member.objects.get(id=member_id)
        if member.status == 'removed':
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def checkstore(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        stores = Store.objects.filter(id=store_id)
        if stores.count() > 0:
            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getInstagram(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        member = Member.objects.get(id=member_id)
        instagram = member.instagram
        resp = {'result_code':'0', 'instagram':instagram}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def deleteProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        products = Product.objects.filter(id=product_id)
        if products.count() > 0:
            product = products[0]

            fs = FileSystemStorage()

            ppictures = ProductPicture.objects.filter(product_id=product.pk)
            for ppicture in ppictures:
                fname = ppicture.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
                ppicture.delete()

            psaves = ProductSave.objects.filter(product_id=product.pk)
            for psave in psaves:
                psave.delete()

            product.delete()

        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))



















###########################  Admin  #######################################################################################################################################################################################

def loginpage(request):
    try:
        if request.session['status'] != '':
            return redirect('/home')
    except KeyError:
        print('no session')
    return render(request, 'qhome/login.html')

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def adminloginprocess(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        accounts = Account.objects.filter(email=email, password=password)
        if accounts.count() > 0:
            account = accounts[0]
            members = Member.objects.filter(email=email, password=password)
            member = None
            if members.count() == 0:
                member = Member()
                member.name = 'Admin'
                member.email = email
                member.password = password
                member.phone_number = account.phone_number
                member.role = 'admin'
                member.save()
            else:
                member = members[0]
            if member is not None: request.session['admin'] = member.pk
            stores = Store.objects.all().order_by('-id')
            request.session['status'] = 'loggedin'
            return render(request, 'qhome/home.html', {'stores':getStoreList(stores), 'member':member})
        else:
            return render(request, 'qhome/result.html',
                          {'response': 'You don\'t have any permission to access this site. Try again with another credential.'})
    elif request.method == 'GET':
        return redirect('/home')
    else:
        return redirect('/home')


def logout(request):
    request.session['status'] = ''
    return render(request, 'qhome/login.html')

def getStoreList(stores):
    storeList = []
    for store in stores:
        if int(store.member_id) > 0:
            membs = Member.objects.filter(id=store.member_id)
            if membs.count() > 0:
                memb = membs[0]
                store.member_name = memb.name
                stlikes = StoreLike.objects.filter(store_id=store.pk)
                store.likes = str(stlikes.count())
                storeList.append(store)
    return storeList

def home(request):
    if request.session['status'] == '':
        return redirect('/logout')
    member = Member.objects.get(id=request.session['admin'])
    stores = Store.objects.all().order_by('-id')
    storeList = []
    for store in stores:
        if store.status2 == '':
            storeList.append(store)
    return render(request, 'qhome/home.html', {'stores':getStoreList(storeList), 'member':member})

def info(request):
    lang = request.GET['lang']
    text = request.GET['text']
    return render(request, 'qhome/info.html', {'text':text, 'lang':lang})

def adminNotifications(request):
    if request.session['status'] == '':
        return redirect('/logout')
    return render(request, 'qhome/notifications.html')

def stores(request):
    store_id = request.GET['store_id']
    if request.session['status'] == '':
        return redirect('/logout')
    member = Member.objects.get(id=request.session['admin'])
    stores = Store.objects.all().order_by('-id')
    storeList = []
    for store in stores:
        if store.status2 == '':
            storeList.append(store)
    return render(request, 'qhome/home.html', {'stores':getStoreList(storeList), 'member':member, 'store_id':store_id})


def approvestore(request):

    if request.session['status'] == '':
        return redirect('/logout')

    store_id = request.GET['store_id']

    store = Store.objects.get(id=store_id)
    store.status = 'approved'
    store.save()

    stores = Store.objects.filter(member_id=store.member_id, status='approved')
    members = Member.objects.filter(id=store.member_id)
    if members.count() > 0:
        member = members[0]
        member.stores = str(stores.count())
        member.save()

    info = 'Congratulations! Your store has been verified. You can upload lots of products on the store for sale. Please let us know if you have any questions\nHave a nice day.\nQhome'
    admin_id = request.session['admin']
    toids = []
    toids.append(store.member_id)
    sendAdminMessage(admin_id, toids, info, '')

    sendFCMPushNotification(store.member_id, admin_id, info)

    return redirect('/home')

def declinestore(request):

    if request.session['status'] == '':
        return redirect('/logout')

    store_id = request.GET['store_id']

    store = Store.objects.get(id=store_id)
    store.status = 'declined'
    store.save()

    stores = Store.objects.filter(member_id=store.member_id, status='approved')
    members = Member.objects.filter(id=store.member_id)
    if members.count() > 0:
        member = members[0]
        member.stores = str(stores.count())
        member.save()

    info = 'Sorry, unfortunately your store has been declined. You will need to update your store.'
    admin_id = request.session['admin']
    toids = []
    toids.append(store.member_id)
    sendAdminMessage(admin_id, toids, info, '')

    sendFCMPushNotification(store.member_id, admin_id, info)

    return redirect('/home')

def producers(request):
    if request.session['status'] == '':
        return redirect('/logout')
    member = Member.objects.get(id=request.session['admin'])
    members = Member.objects.filter(role='producer').order_by('-id')
    memberList = []
    for memb in members:
        if memb.status == '':
            memberList.append(memb)

    return render(request, 'qhome/producers.html', {'producers':getMemberList(memberList), 'member':member})

def getMemberList(members):
    memberList = []
    for member in members:
        stores = Store.objects.filter(member_id=member.pk)
        phones = Phone.objects.filter(member_id=member.pk)
        phoneList=[]
        for phone in phones:
            if phone.phone_number != member.phone_number:
                phoneList.append(phone)
        addresses = Address.objects.filter(member_id=member.pk)
        addressList=[]
        for address in addresses:
            if address.address != member.address:
                addressList.append(address)
        orders = Order.objects.filter(member_id=member.pk).order_by('-id')
        items = OrderItem.objects.filter(producer_id=member.pk).order_by('-id')


        data = {
            'id': member.pk,
            'name': member.name,
            'email': member.email,
            'password': member.password,
            'address': member.address,
            'phone_number': member.phone_number,
            'area': member.area,
            'street': member.street,
            'house': member.house,
            'role': member.role,
            'instagram': member.instagram,
            'auth_status': member.auth_status,
            'registered_time': member.registered_time,
            'status': member.status,
            'stores': stores,
            'ordered':orders.count(),
            'received':items.count(),
            'phones':phoneList,
            'phone_count':len(phoneList),
            'addresses':addressList,
            'address_count':len(addressList),
        }

        memberList.append(data)
    return memberList

def likes(request):
    if request.session['status'] == '':
        return redirect('/logout')
    store_id = request.GET['store_id']
    store = Store.objects.get(id=store_id)
    sls = StoreLike.objects.filter(store_id=store_id)
    likeList = []
    for sl in sls:
        likes = Member.objects.filter(id=sl.member_id)
        if likes.count() > 0:
            like = likes[0]
            likeList.append(like)

    request.session['store'] = store_id

    return render(request, 'qhome/likes.html', {'likes':getMemberList(likeList), 'store':store})


def viewrole(request):
    if request.session['status'] == '':
        return redirect('/logout')
    member_id = request.GET['member_id']
    member = Member.objects.get(id=member_id)
    if member.role == 'producer':
        members = Member.objects.filter(role='producer').order_by('-id')
        return render(request, 'qhome/producers.html', {'producers':getMemberList(members), 'member_id':member_id})
    else:
        members = Member.objects.filter(role='customer').order_by('-id')
        return render(request, 'qhome/customers.html', {'users':getMemberList(members), 'member_id':member_id})

def reviews(request):
    if request.session['status'] == '':
        return redirect('/logout')
    store_id = request.GET['store_id']
    ratings = Rating.objects.filter(store_id=store_id)
    ratingList = []
    for rating in ratings:
        members = Member.objects.filter(id=rating.member_id)
        if members.count() > 0:
            member = members[0]
            data = {
                'id': rating.pk,
                'store_id': rating.store_id,
                'member_id':rating.member_id,
                'member_name':rating.member_name,
                'member_email': member.email,
                'member_phone': member.phone_number,
                'rating': rating.rating,
                'date_time': rating.date_time,
                'subject': rating.subject,
                'description': rating.description,
                'lang': rating.lang,
            }
            ratingList.append(data)

    store = Store.objects.get(id=store_id)

    return render(request, 'qhome/store_reviews.html', {'ratings':ratingList, 'store':store})


def customers(request):
    if request.session['status'] == '':
        return redirect('/logout')
    member = Member.objects.get(id=request.session['admin'])
    members = Member.objects.all().order_by('-id')
    memberList = []
    for memb in members:
        if memb.role != 'admin' and memb.status == '':
            memberList.append(memb)

    return render(request, 'qhome/customers.html', {'users':getMemberList(memberList), 'member':member})


def users(request):
    member_id = request.GET['user_id']
    if request.session['status'] == '':
        return redirect('/logout')
    member = Member.objects.get(id=request.session['admin'])
    members = Member.objects.all().order_by('-id')
    memberList = []
    for memb in members:
        if memb.role != 'admin' and memb.status == '':
            memberList.append(memb)
    return render(request, 'qhome/customers.html', {'users':getMemberList(memberList), 'member':member, 'member_id':member_id})


def products(request):
    if request.session['status'] == '':
        return redirect('/logout')
    store_id = request.GET['store_id']
    store = Store.objects.get(id=store_id)
    products = Product.objects.filter(store_id=store_id)
    productList = []
    for product in products:
        ois = OrderItem.objects.filter(product_id=product.pk)
        orderedList = []
        soldList = []
        for oi in ois:
            if oi.status == 'delivered' and oi.status2 != 'canceled':
                soldList.append(oi)
            elif oi.status != 'delivered' and oi.status2 != 'canceled':
                orderedList.append(oi)
        product.ordereds = str(len(orderedList))
        product.solds = str(len(soldList))
        pictures = ProductPicture.objects.filter(product_id=product.pk)

        data={
            'id':product.id,
            'store_id':product.store_id,
            'member_id':product.member_id,
            'name':product.name,
            'picture_url':product.picture_url,
            'category':product.category,
            'price':product.price,
            'new_price':product.new_price,
            'unit':product.unit,
            'description':product.description,
            'registered_time':product.registered_time,
            'status':product.status,
            'likes':product.likes,
            'isLiked':product.isLiked,
            'ar_name':product.ar_name,
            'ar_category':product.ar_category,
            'ar_description':product.ar_description,
            'ordereds':product.ordereds,
            'solds':product.solds,
            'store_name':product.store_name,
            'ar_store_name':product.ar_store_name,
            'pictures':pictures,
        }

        productList.append(data)

    return render(request, 'qhome/products.html', {'products':productList, 'store':store})


def receivedorders(request):
    if request.session['status'] == '':
        return redirect('/logout')
    producer_id = request.GET['producer_id']
    itemsList = []
    items = OrderItem.objects.filter(producer_id=producer_id).order_by('-id')
    for item in items:
        orders = Order.objects.filter(id=item.order_id)
        if orders.count() > 0:
            order = orders[0]
            item.orderID = order.orderID
            item.contact = order.phone_number
            member = None
            if int(item.member_id) > 0:
                member = Member.objects.get(id=item.member_id)
            else:
                member = Member()
                member.id = 0
                member.name = ''

            data = {
                'id': item.pk,
                'order_id': item.order_id,
                'member_id':item.member_id,
                'producer_id': item.producer_id,
                'store_id': item.store_id,
                'store_name': item.store_name,
                'ar_store_name': item.ar_store_name,
                'product_id': item.product_id,
                'product_name': item.product_name,
                'ar_product_name': item.ar_product_name,
                'category': item.category,
                'ar_category': item.ar_category,
                'price': item.price,
                'unit': item.unit,
                'quantity': item.quantity,
                'date_time': item.date_time,
                'picture_url': item.picture_url,
                'status': item.status,
                'status2': item.status2,
                'discount': item.discount,
                'status_time': item.status_time,
                'order': order,
                'member': member,
            }

            itemsList.append(data)

    producer = Member.objects.get(id=producer_id)

    return render(request, 'qhome/received_orders.html', {'items':itemsList, 'producer':producer})




def orders(request):
    if request.session['status'] == '':
        return redirect('/logout')
    member_id = request.GET['user_id']
    member = Member.objects.get(id=member_id)
    orders = Order.objects.filter(member_id=member_id).order_by('-id')

    return render(request, 'qhome/orders.html', {'orders':orderData(orders), 'user':member})


def items(request):
    if request.session['status'] == '':
        return redirect('/logout')
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)
    itemsList = []
    items = OrderItem.objects.filter(order_id=order_id).order_by('-id')
    for item in items:
        member = None
        if int(item.member_id) > 0:
            members = Member.objects.filter(id=item.member_id)
            if members.count() > 0:
                member = members[0]
        else:
            member = Member()
            member.id = 0
            member.name = ''

        data = {
            'id': item.pk,
            'order_id': item.order_id,
            'member_id':item.member_id,
            'producer_id': item.producer_id,
            'store_id': item.store_id,
            'store_name': item.store_name,
            'ar_store_name': item.ar_store_name,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'ar_product_name': item.ar_product_name,
            'category': item.category,
            'ar_category': item.ar_category,
            'price': item.price,
            'unit': item.unit,
            'quantity': item.quantity,
            'date_time': item.date_time,
            'picture_url': item.picture_url,
            'status': item.status,
            'status2': item.status2,
            'discount': item.discount,
            'status_time': item.status_time,
            'member': member,
        }

        itemsList.append(data)

    return render(request, 'qhome/order_items.html', {'items':itemsList, 'order':order})


def salehistory(request):
    if request.session['status'] == '':
        return redirect('/logout')
    product_id = request.GET['product_id']
    option = request.GET['option']
    itemsList = []
    items = OrderItem.objects.filter(product_id=product_id).order_by('-id')
    for item in items:
        orders = Order.objects.filter(id=item.order_id)
        if orders.count() > 0:
            order = orders[0]
            item.orderID = order.orderID
            item.contact = order.phone_number
            member = None
            if int(item.member_id) > 0:
                members = Member.objects.filter(id=item.member_id)
                if members.count() > 0:
                    member = members[0]
            else:
                member = Member()
                member.id = 0
                member.name = ''

            data = {
                'id': item.pk,
                'order_id': item.order_id,
                'member_id':item.member_id,
                'producer_id': item.producer_id,
                'store_id': item.store_id,
                'store_name': item.store_name,
                'ar_store_name': item.ar_store_name,
                'product_id': item.product_id,
                'product_name': item.product_name,
                'ar_product_name': item.ar_product_name,
                'category': item.category,
                'ar_category': item.ar_category,
                'price': item.price,
                'unit': item.unit,
                'quantity': item.quantity,
                'date_time': item.date_time,
                'picture_url': item.picture_url,
                'status': item.status,
                'status2': item.status2,
                'discount': item.discount,
                'status_time': item.status_time,
                'order': order,
                'member': member,
            }

            if option == 'sold':
                if item.status == 'delivered':
                    itemsList.append(data)
            elif option == 'ordered':
                if item.status != 'delivered' and item.status2 != 'canceled':
                    itemsList.append(data)
            else:
                itemsList.append(data)

    product = Product.objects.get(id=product_id)

    return render(request, 'qhome/sale_history.html', {'items':itemsList, 'product':product, 'option':option})


def productpictures(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    pictures = ProductPicture.objects.filter(product_id=product_id)

    return render(request, 'qhome/gallery.html', {'pictures':pictures, 'product':product})


def advertisepage(request):
    stores = Store.objects.filter(status='approved').order_by('-id')
    ad = None
    ads = Advertisement.objects.filter(id=1)
    if ads.count() == 0:
        ad = Advertisement()
        ad.store1 = ''
        ad.store2 = ''
        ad.store3 = ''
        ad.save()
    else:
        ad = ads[0]
    return render(request, 'qhome/advertise.html', {'stores':getStoreList(stores), 'ad':ad})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def submitadvertisement(request):

    if request.method == 'POST':

        fs = FileSystemStorage()

        isNewF = False;

        store1 = request.POST.get('store1', '')
        store2 = request.POST.get('store2', '')
        store3 = request.POST.get('store3', '')

        ad = Advertisement.objects.get(id=1)

        photo1 = None
        photo2 = None
        photo3 = None

        try:
            photo1 = request.FILES['photo1']
            if store1 == '':
                return render(request, 'qhome/result.html', {'response': 'Please select a store for advertisement1.'})
            try:
                x1 = request.POST.get('x1', '0')
                y1 = request.POST.get('y1', '0')
                w1 = request.POST.get('w1', '32')
                h1 = request.POST.get('h1', '32')
                #  return HttpResponse(w)
                photo1 = picture_process(photo1, x1, y1, w1, h1)

            except MultiValueDictKeyError:
                print('No cropping')
            except ValueError:
                print('No cropping')

            filename1 = fs.save(photo1.name, photo1)
            uploaded_file_url1 = fs.url(filename1)
            ad.picture1 = settings.URL + uploaded_file_url1

        except MultiValueDictKeyError:
            print('No exists')

        try:
            photo2 = request.FILES['photo2']
            if store2 == '':
                return render(request, 'qhome/result.html', {'response': 'Please select a store for advertisement2.'})

            try:
                x2 = request.POST.get('x2', '0')
                y2 = request.POST.get('y2', '0')
                w2 = request.POST.get('w2', '32')
                h2 = request.POST.get('h2', '32')
                #  return HttpResponse(w2)
                photo2 = picture_process(photo2, x2, y2, w2, h2)

            except MultiValueDictKeyError:
                print('No cropping')
            except ValueError:
                print('No cropping')

            filename2 = fs.save(photo2.name, photo2)
            uploaded_file_url2 = fs.url(filename2)
            ad.picture2 = settings.URL + uploaded_file_url2

        except MultiValueDictKeyError:
            print('No exists')

        try:
            photo3 = request.FILES['photo3']
            if store3 == '':
                return render(request, 'qhome/result.html', {'response': 'Please select a store for advertisement3.'})
            try:
                x3 = request.POST.get('x3', '0')
                y3 = request.POST.get('y3', '0')
                w3 = request.POST.get('w3', '32')
                h3 = request.POST.get('h3', '32')
                #  return HttpResponse(w3)
                photo3 = picture_process(photo3, x3, y3, w3, h3)

            except MultiValueDictKeyError:
                print('No cropping')
            except ValueError:
                print('No cropping')

            filename3 = fs.save(photo3.name, photo3)
            uploaded_file_url3 = fs.url(filename3)
            ad.picture3 = settings.URL + uploaded_file_url3

        except MultiValueDictKeyError:
            print('No exists')


        if store1 != '':
            if ad.picture1 == '':
                return render(request, 'qhome/result.html', {'response': 'Please upload a picture for advertisement1.'})
            ad.store1 = store1
            store = Store.objects.get(id=int(store1))
            ad.stname1 = store.name + '\n' + " (" + store.ar_name + ")"

        if store2 != '':
            if ad.picture2 == '':
                return render(request, 'qhome/result.html', {'response': 'Please upload a picture for advertisement2.'})
            ad.store2 = store2
            store = Store.objects.get(id=int(store2))
            ad.stname2 = store.name + '\n' + " (" + store.ar_name + ")"

        if store3 != '':
            if ad.picture3 == '':
                return render(request, 'qhome/result.html', {'response': 'Please upload a picture for advertisement3.'})
            ad.store3 = store3
            store = Store.objects.get(id=int(store3))
            ad.stname3 = store.name + '\n' + " (" + store.ar_name + ")"

        if ad.picture1 == '' and ad.picture2 == '' and ad.picture3 == '':
            if photo1 is None and photo2 is None and photo3 is None:
                    return render(request, 'qhome/result.html', {'response': 'Please upload at least one picture for advertisement.'})

        if store1 == '' and store2 == '' and store3 == '': return render(request, 'qhome/result.html', {'response': 'Please select at least one store for advertisement.'})

        ad.save()

        stores = Store.objects.filter(status='approved').order_by('-id')
        return render(request, 'qhome/advertise.html', {'stores':getStoreList(stores), 'ad':ad})


from PIL import Image
from django.core.files.uploadedfile import *

def picture_process(image, x, y, w, h):
    # return HttpResponse(w)
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    # return HttpResponse(w)
    file = None
    try:
        thumb_io = io.BytesIO()
        image_file = Image.open(image)
        # resized_image = image_file.resize((600, int(250 * image_file.height / image_file.width)), Image.ANTIALIAS)
        cropped_image = image_file.crop((x, y, w + x, h + y))
        # resized_image = cropped_image.resize((160, 160), Image.ANTIALIAS)
        cropped_image.save(thumb_io, image.content_type.split('/')[-1].upper())

        # creating new InMemoryUploadedFile() based on the modified file
        file = InMemoryUploadedFile(thumb_io,
            u"photo", # important to specify field name here
            "croppedimage.jpg",
            image.content_type,
            None, None)
    except OSError:
        print('Invalid file!')

    return file


def resetAds(request):
    stores = Store.objects.filter(status='approved').order_by('-id')
    fs = FileSystemStorage()
    ads = Advertisement.objects.filter(id=1)
    ad = ads[0]
    ad.store1 = ''
    ad.stname1 = ''
    ad.store2 = ''
    ad.stname2 = ''
    ad.store3 = ''
    ad.stname3 = ''
    fname = ad.picture1.replace(settings.URL + '/media/', '')
    fs.delete(fname)
    ad.picture1 = ''
    fname = ad.picture2.replace(settings.URL + '/media/', '')
    fs.delete(fname)
    ad.picture2 = ''
    fname = ad.picture3.replace(settings.URL + '/media/', '')
    fs.delete(fname)
    ad.picture3 = ''
    ad.save()

    return render(request, 'qhome/advertise.html', {'stores':getStoreList(stores), 'ad':ad})


def cancelad(request):
    ad_num = request.GET['ad']

    stores = Store.objects.filter(status='approved').order_by('-id')

    fs = FileSystemStorage()
    ads = Advertisement.objects.filter(id=1)
    ad = ads[0]

    if int(ad_num) == 1:
        ad.store1 = ''
        ad.stname1 = ''
        fname = ad.picture1.replace(settings.URL + '/media/', '')
        fs.delete(fname)
        ad.picture1 = ''
    elif int(ad_num) == 2:
        ad.store2 = ''
        ad.stname2 = ''
        fname = ad.picture2.replace(settings.URL + '/media/', '')
        fs.delete(fname)
        ad.picture2 = ''
    elif int(ad_num) == 3:
        ad.store3 = ''
        ad.stname3 = ''
        fname = ad.picture3.replace(settings.URL + '/media/', '')
        fs.delete(fname)
        ad.picture3 = ''

    ad.save()

    return render(request, 'qhome/advertise.html', {'stores':getStoreList(stores), 'ad':ad})


def couponpage(request):
    coupons  = Coupon.objects.all()
    for coupon in coupons:
        current = int(round(time.time() * 1000))
        if current > int(coupon.expire_time):
            coupon.status = 'expired'
        useds = UsedCoupon.objects.filter(coupon_id=coupon.pk)
        if coupon.status != 'expired':
            coupon.status = str(useds.count()) + " " + "Used"
    return render(request, 'qhome/coupon.html', {'coupons':coupons})

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def createCoupon(request):
    if request.method == 'POST':
        discount = request.POST.get('discount', '0')
        months = request.POST.get('month', '0')
        days = request.POST.get('day', '0')
        hours = request.POST.get('hour', '0')

        if int(discount) == 0: return render(request, 'qhome/result.html', {'response': 'Discount value should not be 0. Please enter discount value.'})
        if int(months) == 0 and int(days) == 0 and int(hours) == 0:
            return render(request, 'qhome/result.html', {'response': 'Lifespan value should not be 0. Please enter available lifespan value.'})

        coupon = Coupon()
        coupon.discount = discount
        lifespanMilisecs = (int(months) * 30 * 86400 + int(days) * 86400 + int(hours) * 3600) * 1000
        coupon.expire_time = str(int(round(time.time() * 1000)) + lifespanMilisecs)
        coupon.save()

        return redirect('/couponpage')

def delcoupon(request):
    coupon_id = request.GET['coupon_id']
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('/couponpage')


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def adminmessage(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        message = request.POST.get('message', '')
        image = request.POST.get('image', '')

        if int(member_id) > 0:

            admin_id = request.session['admin']
            toids = []
            toids.append(member_id)
            sendAdminMessage(admin_id, toids, message, image)

            sendFCMPushNotification(member_id, admin_id, message)

            member = Member.objects.get(id=member_id)

            return render(request, 'qhome/result.html',
                              {'response': 'Message sent to ' + member.name})

        else:

            admin_id = request.session['admin']
            toids = []
            members = Member.objects.all()
            for member in members:
                if member.pk != admin_id:
                    toids.append(member.pk)
            adminBroadcast(admin_id, toids, message, image)

            return render(request, 'qhome/result.html',
                              {'response': 'Message sent to all Qhome members'})



def qhomeReviews(request):
    ratings = Rating.objects.filter(store_id=0)
    ratingList = []
    s = 0
    for rating in ratings:
        s = s + float(rating.rating)
        members = Member.objects.filter(id=rating.member_id)
        if members.count() > 0:
            member = members[0]
            data = {
                'id': rating.pk,
                'store_id': rating.store_id,
                'member_id':rating.member_id,
                'member_name':rating.member_name,
                'member_email': member.email,
                'member_phone': member.phone_number,
                'rating': rating.rating,
                'date_time': rating.date_time,
                'subject': rating.subject,
                'description': rating.description,
                'lang': rating.lang,
            }
            ratingList.append(data)

    qrating = 0.0

    if ratings.count() > 0 :
        qrating = float(s/ratings.count())

    qrating = round(qrating, 1)

    return render(request, 'qhome/feedback.html', {'ratings':ratingList, 'qrating': qrating})


def luckypurchases(request):
    if request.session['status'] == '':
        return redirect('/logout')

    order_id = request.GET['order_id']

    orders = Order.objects.all().order_by('-id')

    #  order date time limited to today

    orderList = []
    now = int(round(time.time()))
    date = datetime.datetime.fromtimestamp(now)
    nowDay = date.day
    nowMonth = date.month
    nowYear = date.year
    for order in orders:
        order_date = datetime.datetime.fromtimestamp(int(int(order.date_time)/1000))
        day = order_date.day
        month = order_date.month
        year = order_date.year
        if day == nowDay and month == nowMonth and year == nowYear:
            if int(order.member_id) > 0:
                orderList.append(order)

    return render(request, 'qhome/lucky_purchase.html', {'orders':orderData(orderList), 'order_id':order_id})


def drawpurchase(request):
    if request.session['status'] == '':
        return redirect('/logout')

    orders = Order.objects.all().order_by('-id')

    orderList = []
    orderidList = []
    todayLuckyDraw = False
    now = int(round(time.time()))
    date = datetime.datetime.fromtimestamp(now)
    nowDay = date.day
    nowMonth = date.month
    nowYear = date.year
    for order in orders:
        order_date = datetime.datetime.fromtimestamp(int(int(order.date_time)/1000))
        day = order_date.day
        month = order_date.month
        year = order_date.year
        if day == nowDay and month == nowMonth and year == nowYear:
            if int(order.member_id) > 0:
                orderList.append(order)
                orderidList.append(order.pk)
                winners = Winner.objects.filter(order_id=order.pk)
                if winners.count() > 0: todayLuckyDraw = True

    if len(orderList) == 0:
        return render(request, 'qhome/result.html',
                              {'response': 'Unfortunately, time has already been expired. Please refresh.'})

    index = 0
    order_id = 0

    if todayLuckyDraw == False:
        for x in range(len(orderList) * 100):
            index = random.randint(1, len(orderidList))
        if index > 0:
            order_id = orderidList[index - 1]
            winners = Winner.objects.filter(order_id=order_id)

            if winners.count() == 0:

                orders = Order.objects.filter(id=order_id)
                if orders.count() > 0:
                    order = orders[0]
                    winner = Winner()
                    winner.order_id = order_id
                    winner.won_time = str(int(round(time.time() * 1000)))
                    winner.save()
                    admin_id = request.session['admin']
                    toids = []
                    toids.append(order.member_id)
                    items = OrderItem.objects.filter(order_id=order_id)
                    info = 'Congratulations! You have won this order!\n' + 'Order ID: ' + order.orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(order.date_time) / 1000.0)) + '\n' + 'Price: ' + order.price + ' QR' + '\n' + 'Items: ' + str(items.count()) + '\n' + 'Qhome Lucky Draw System'
                    sendAdminMessage(admin_id, toids, info, settings.URL + '/static/qhome/images/winner2.png')

                    sendFCMPushNotification(order.member_id, admin_id, info)

    return render(request, 'qhome/lucky_purchase.html', {'orders':orderData(orderList), 'order_id':order_id})


    #  order date time limited to today

    # orderList = []
    # now = int(round(time.time()))
    # date = datetime.datetime.fromtimestamp(now)
    # nowDay = date.day
    # nowMonth = date.month
    # nowYear = date.year
    # for order in orders:
    #     order_date = datetime.datetime.fromtimestamp(int(int(order.date_time)/1000))
    #     day = order_date.day
    #     month = order_date.month
    #     year = order_date.year
    #     if day == nowDay and month == nowMonth and year == nowYear:
    #         if int(order.member_id) > 0:
    #             orderList.append(order)

    # return render(request, 'qhome/lucky_purchase.html', {'orders':orderData(orderList), 'order_id':order_id})


def notis(request):
    notifications = Notification.objects.all().order_by('-id')
    notiList = []
    admin_id = request.session['admin']
    for noti in notifications:
        if int(noti.receiver_id) == admin_id:
            receivers = Member.objects.filter(id=noti.receiver_id)
            if receivers.count() > 0:
                receiver = receivers[0]
                senders = Member.objects.filter(id=noti.sender_id)
                if senders.count() > 0:
                    sender = senders[0]
                    data = {
                        'id':noti.pk,
                        'receiver': receiver,
                        'sender': sender,
                        'date_time': noti.date_time,
                        'message': noti.message,
                        'image_message': noti.image_message,
                    }
                    notiList.append(data)

    return render(request, 'qhome/notis.html', {'notis':notiList})


def delAdminNotification(request):
    notid = request.GET['noti_id']
    noti = Notification.objects.get(id=notid)
    noti.delete()
    return redirect('/notis')


def todayLuckyInfo(request):

    if request.session['status'] == '':
        return redirect('/logout')

    info_id = request.GET['info_id']

    infos = Info.objects.all().order_by('-id')
    now = int(round(time.time()))
    date = datetime.datetime.fromtimestamp(now)
    nowDay = date.day
    nowMonth = date.month
    nowYear = date.year

    infoList = []
    for info in infos:
        info_date = datetime.datetime.fromtimestamp(int(int(info.date_time)/1000))
        day = info_date.day
        month = info_date.month
        year = info_date.year
        if day == nowDay and month == nowMonth and year == nowYear:
            if int(info.member_id) > 0:
                members = Member.objects.filter(id=info.member_id)
                if members.count() > 0:
                    member = members[0]
                    data = {
                        'id': info.id,
                        'member': memberInfo(member),
                        'date_time': info.date_time,
                        'status': info.status,
                    }

                    infoList.append(data)

    return render(request, 'qhome/lucky_info.html', {'infos':infoList, 'info_id':info_id})


def memberInfo(member):
    stores = Store.objects.filter(member_id=member.pk)
    phones = Phone.objects.filter(member_id=member.pk)
    phoneList=[]
    for phone in phones:
        if phone.phone_number != member.phone_number:
            phoneList.append(phone)
    addresses = Address.objects.filter(member_id=member.pk)
    addressList=[]
    for address in addresses:
        if address.address != member.address:
            addressList.append(address)
    orders = Order.objects.filter(member_id=member.pk).order_by('-id')
    items = OrderItem.objects.filter(producer_id=member.pk).order_by('-id')


    data = {
        'id': member.pk,
        'name': member.name,
        'email': member.email,
        'password': member.password,
        'address': member.address,
        'phone_number': member.phone_number,
        'area': member.area,
        'street': member.street,
        'house': member.house,
        'role': member.role,
        'instagram': member.instagram,
        'auth_status': member.auth_status,
        'registered_time': member.registered_time,
        'status': member.status,
        'stores': stores,
        'ordered':orders.count(),
        'received':items.count(),
        'phones':phoneList,
        'phone_count':len(phoneList),
        'addresses':addressList,
        'address_count':len(addressList),
    }

    return data


def drawInfo(request):
    if request.session['status'] == '':
        return redirect('/logout')

    info_id = request.GET['info_id']

    infos = Info.objects.all().order_by('-id')
    now = int(round(time.time()))
    date = datetime.datetime.fromtimestamp(now)
    nowDay = date.day
    nowMonth = date.month
    nowYear = date.year

    infoList = []
    toids = []
    for info in infos:
        info_date = datetime.datetime.fromtimestamp(int(int(info.date_time)/1000))
        day = info_date.day
        month = info_date.month
        year = info_date.year
        if day == nowDay and month == nowMonth and year == nowYear:
            if int(info_id) != int(info.member_id): toids.append(info.member_id)
            members = Member.objects.filter(id=info.member_id)
            if members.count() > 0:
                member = members[0]
                data = {
                    'id': info.id,
                    'member': memberInfo(member),
                    'date_time': info.date_time,
                    'status': info.status,
                }

                infoList.append(data)

    if len(infoList) == 0:
        return render(request, 'qhome/result.html',
                              {'response': 'Unfortunately, time has already been expired. Please refresh.'})

    info = Info.objects.get(id=info_id)
    info.status = 'won'
    info.save()

    admin_id = request.session['admin']
    members = Member.objects.filter(id=info.member_id)
    if members.count() > 0:
        member = members[0]
        message = 'Congratulations! You have won today! You are blessed largely today. Have a good day.\n' + 'Qhome Lucky Draw System'
        memberids = []
        memberids.append(member.pk)
        sendAdminMessage(admin_id, memberids, message, settings.URL + '/static/qhome/images/winner.png')

        sendFCMPushNotification(member.pk, admin_id, message)

        message = 'Thanks for your waiting for being a winner today. ' + member.name + ' has won today\'s lucky draw. Please try again tomorrow. Have a good day.\n' + 'Qhome Lucky Draw System'
        sendAdminMessage(admin_id, toids, message, '')

        for toid in toids:
            sendFCMPushNotification(toid, admin_id, message)

    return redirect('/todayLuckyInfo?info_id=' + info_id)


def adminsetting(request):
    if request.session['status'] == '':
        return redirect('/logout')
    accounts = Account.objects.filter(id=1)
    if accounts.count() == 0:
        account = Account()
        account.save()
    else: account = accounts[0]
    return  render(request, 'qhome/setting.html', {'admin':account})



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def editaccount(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '')

        account = Account.objects.get(id=1)
        account.email = email
        account.password = password
        account.phone_number = phone

        account.save()

        if request.session['admin'] is not None:
            member = Member.objects.get(id=int(request.session['admin']))
            member.email = email
            member.password = password
            member.phone_number = phone
            member.save()

            notifications = Notification.objects.filter(sender_name='Qhome')
            for noti in notifications:
                noti.sender_email = email
                noti.sender_phone = phone
                noti.save()

        return  render(request, 'qhome/setting.html', {'admin':account, 'note':'account_updated'})


def removestore(request):
    store_id = request.GET['store_id']

    fs = FileSystemStorage()
    store = Store.objects.get(id=store_id)

    members = Member.objects.filter(id=store.member_id)
    if members.count() > 0:
        member = members[0]
        if int(member.stores) > 0:
            if int(member.stores) > 0:
                member.stores = str(int(member.stores) - 1)
                member.save()

    slikes = StoreLike.objects.filter(store_id=store_id)
    for slike in slikes:
        slike.delete()

    products = Product.objects.filter(store_id=store_id)
    for product in products:
        ppictures = ProductPicture.objects.filter(product_id=product.pk)
        for ppicture in ppictures:
            fname = ppicture.picture_url.replace(settings.URL + '/media/', '')
            fs.delete(fname)
            ppicture.delete()

        psaves = ProductSave.objects.filter(product_id=product.pk)
        for psave in psaves:
            psave.delete()

        product.delete()

    ratings = Rating.objects.filter(store_id=store_id)
    for rating in ratings:
        rating.delete()

    cartitems = CartItem.objects.filter(store_id=store_id)
    for citem in cartitems:
        citem.delete()

    orderitems = OrderItem.objects.filter(store_id=store_id)
    for oitem in orderitems:
        winners = Winner.objects.filter(order_id=oitem.order_id)
        for winner in winners:
            winner.delete()
        orders = Order.objects.filter(id=oitem.order_id)
        if orders.count() > 0:
            order = orders[0]
            items = OrderItem.objects.filter(order_id=order.pk)
            if items.count() <= 1:
                order.delete()
        fname = oitem.picture_url.replace(settings.URL + '/media/', '')
        fs.delete(fname)
        oitem.delete()

    fname = store.logo_url.replace(settings.URL + '/media/', '')
    fs.delete(fname)
    store.delete()

    return redirect('/home')


def removemember(request):
    member_id = request.GET['member_id']
    member = Member.objects.get(id=member_id)

    fs = FileSystemStorage()

    stores = Store.objects.filter(member_id=member.pk)
    for store in stores:
        store_id = store.pk
        slikes = StoreLike.objects.filter(store_id=store_id)
        for slike in slikes:
            slike.delete()

        products = Product.objects.filter(store_id=store_id)
        for product in products:
            ppictures = ProductPicture.objects.filter(product_id=product.pk)
            for ppicture in ppictures:
                fname = ppicture.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
                ppicture.delete()

            psaves = ProductSave.objects.filter(product_id=product.pk)
            for psave in psaves:
                psave.delete()

            product.delete()

        ratings = Rating.objects.filter(store_id=store_id)
        for rating in ratings:
            rating.delete()

        cartitems = CartItem.objects.filter(store_id=store_id)
        for citem in cartitems:
            citem.delete()

        orderitems = OrderItem.objects.filter(store_id=store_id)
        for oitem in orderitems:
            winners = Winner.objects.filter(order_id=oitem.order_id)
            for winner in winners:
                winner.delete()
            orders = Order.objects.filter(id=oitem.order_id)
            if orders.count() > 0:
                order = orders[0]
                items = OrderItem.objects.filter(order_id=order.pk)
                if items.count() <= 1:
                    order.delete()
            fname = oitem.picture_url.replace(settings.URL + '/media/', '')
            fs.delete(fname)
            oitem.delete()

        fname = store.logo_url.replace(settings.URL + '/media/', '')
        fs.delete(fname)

        store.delete()


    phones = Phone.objects.filter(member_id=member_id)
    for phone in phones:
        phone.delete()

    addresses = Address.objects.filter(member_id=member_id)
    for address in addresses:
        address.delete()

    usedcoupons = UsedCoupon.objects.filter(member_id=member_id)
    for coupon in usedcoupons:
        coupon.delete()

    notis = Notification.objects.filter(receiver_id=member_id)
    for noti in notis:
        noti.delete()

    ratings = Rating.objects.filter(member_id=member_id)
    for rating in ratings:
        rating.delete()

    notis = Notification.objects.filter(sender_id=member_id)
    for noti in notis:
        noti.delete()

    infos = Info.objects.filter(member_id=member_id)
    for info in infos:
        winners = Winner2.objects.filter(info_id=info.pk)
        for winner in winners:
            winner.delete()

        info.delete()


    member.status = 'removed'
    member.save()

    return redirect('/producers')






























































