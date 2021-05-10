from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from qhome import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^qhome/', include('qhome.urls')),
    # url(r'^$', views.index, name='index'),
    url(r'^registerMember',views.registerMember,  name='registerMember'),
    url(r'^login',views.login,  name='login'),
    url(r'^verify',views.verify,  name='verify'),
    url(r'^registerStore',views.registerStore,  name='registerStore'),
    url(r'^getStores',views.getStores,  name='getStores'),
    url(r'^likeStore',views.likeStore,  name='likeStore'),
    url(r'^unLikeStore',views.unLikeStore,  name='unLikeStore'),
    url(r'^uploadProduct',views.uploadProduct,  name='uploadProduct'),
    url(r'^updateStore',views.updateStore,  name='updateStore'),
    url(r'^getProducts',views.getProducts,  name='getProducts'),
    url(r'^getRatings',views.getRatings,  name='getRatings'),
    url(r'^saveProduct',views.saveProduct,  name='saveProduct'),
    url(r'^unsaveProduct',views.unsaveProduct,  name='unsaveProduct'),
    url(r'^getSavedProducts',views.getSavedProducts,  name='getSavedProducts'),
    url(r'^placeStoreFeedback',views.placeStoreFeedback,  name='placeStoreFeedback'),
    url(r'^getProductPictures',views.getProductPictures,  name='getProductPictures'),
    url(r'^addToCart',views.addToCart,  name='addToCart'),
    url(r'^getCartItems',views.getCartItems,  name='getCartItems'),
    url(r'^delCartItem',views.delCartItem,  name='delCartItem'),
    url(r'^updateCartItemQuantity',views.updateCartItemQuantity,  name='updateCartItemQuantity'),
    url(r'^addCartToWishlist',views.addCartToWishlist,  name='addCartToWishlist'),
    url(r'^productInfo',views.productInfo,  name='productInfo'),
    url(r'^addWishlistToCart',views.addWishlistToCart,  name='addWishlistToCart'),
    url(r'^getPhones',views.getPhones,  name='getPhones'),
    url(r'^getAddresses',views.getAddresses,  name='getAddresses'),
    url(r'^savePhoneNumber',views.savePhoneNumber,  name='savePhoneNumber'),
    url(r'^saveAddress',views.saveAddress,  name='saveAddress'),
    url(r'^delAddress',views.delAddress,  name='delAddress'),
    url(r'^delPhone',views.delPhone,  name='delPhone'),
    url(r'^uploadOrder',views.uploadOrder,  name='uploadOrder'),
    url(r'^getUserOrders',views.getUserOrders,  name='getUserOrders'),
    url(r'^delOrder',views.delOrder,  name='delOrder'),
    url(r'^userOrderItems',views.userOrderItems,  name='userOrderItems'),
    url(r'^updateMember',views.updateMember,  name='updateMember'),
    url(r'^receivedOrderItems',views.receivedOrderItems,  name='receivedOrderItems'),
    url(r'^cancelOrderItem',views.cancelOrderItem,  name='cancelOrderItem'),
    url(r'^progressOrderItem',views.progressOrderItem,  name='progressOrderItem'),
    url(r'^orderById',views.orderById,  name='orderById'),
    url(r'^favoriteStores',views.favoriteStores,  name='favoriteStores'),
    url(r'^placeAppFeedback',views.placeAppFeedback,  name='placeAppFeedback'),
    url(r'^getNotifications',views.getNotifications,  name='getNotifications'),
    url(r'^delNotification',views.delNotification,  name='delNotification'),
    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^rstpwd', views.rstpwd, name='rstpwd'),
    url(r'^getAds',views.getAds,  name='getAds'),
    url(r'^contactAdmin',views.contactAdmin,  name='contactAdmin'),
    url(r'^postLuckyInfo',views.postLuckyInfo,  name='postLuckyInfo'),
    url(r'^getMyLuckyInfo',views.getMyLuckyInfo,  name='getMyLuckyInfo'),
    url(r'^regGuest',views.regGuest,  name='regGuest'),
    url(r'^forGuestNotifications',views.forGuestNotifications,  name='forGuestNotifications'),
    url(r'^upProduct',views.uploadProduct2,  name='uploadProduct2'),
    url(r'^uploadfcmtoken',views.fcm_insert,  name='fcm_insert'),
    url(r'^fcmsend',views.sendFCMPushNotification,  name='sendFCMPushNotification'),
    url(r'^getInstagram',views.getInstagram,  name='getInstagram'),
    url(r'^proddelete',views.deleteProduct,  name='deleteProduct'),




    ###### admin

    url(r'^$', views.loginpage, name='loginpage'),
    url(r'^signinprocess',views.adminloginprocess,  name='adminloginprocess'),
    url(r'^logout',views.logout,  name='logout'),
    url(r'^home',views.home,  name='home'),
    url(r'^info',views.info,  name='info'),
    url(r'^adminNotifications',views.adminNotifications,  name='adminNotifications'),
    url(r'^stores',views.stores,  name='stores'),
    url(r'^approvestore',views.approvestore,  name='approvestore'),
    url(r'^declinestore',views.declinestore,  name='declinestore'),
    url(r'^producers',views.producers,  name='producers'),
    url(r'^likes',views.likes,  name='likes'),
    url(r'^viewrole',views.viewrole,  name='viewrole'),
    url(r'^reviews',views.reviews,  name='reviews'),
    url(r'^customers',views.customers,  name='customers'),
    url(r'^users',views.users,  name='users'),
    url(r'^products',views.products,  name='products'),
    url(r'^receivedorders',views.receivedorders,  name='receivedorders'),
    url(r'^orders',views.orders,  name='orders'),
    url(r'^items',views.items,  name='items'),
    url(r'^salehistory',views.salehistory,  name='salehistory'),
    url(r'^productpictures',views.productpictures,  name='productpictures'),
    url(r'^advertisepage',views.advertisepage,  name='advertisepage'),
    url(r'^submitadvertisement',views.submitadvertisement,  name='submitadvertisement'),
    url(r'^submitadvertisement',views.submitadvertisement,  name='submitadvertisement'),
    url(r'^couponpage',views.couponpage,  name='couponpage'),
    url(r'^createCoupon',views.createCoupon,  name='createCoupon'),
    url(r'^delcoupon',views.delcoupon,  name='delcoupon'),
    url(r'^getCoupons',views.getCoupons,  name='getCoupons'),
    url(r'^adminmessage',views.adminmessage,  name='adminmessage'),
    url(r'^qhomeReviews',views.qhomeReviews,  name='qhomeReviews'),
    url(r'^luckypurchases',views.luckypurchases,  name='luckypurchases'),
    url(r'^drawpurchase',views.drawpurchase,  name='drawpurchase'),
    url(r'^resetAds',views.resetAds,  name='resetAds'),
    url(r'^notis',views.notis,  name='notis'),
    url(r'^delAdminNotification',views.delAdminNotification,  name='delAdminNotification'),
    url(r'^todayLuckyInfo',views.todayLuckyInfo,  name='todayLuckyInfo'),
    url(r'^drawInfo',views.drawInfo,  name='drawInfo'),
    url(r'^cancelad',views.cancelad,  name='cancelad'),
    url(r'^adminsetting',views.adminsetting,  name='adminsetting'),
    url(r'^editaccount',views.editaccount,  name='editaccount'),
    url(r'^removestore',views.removestore,  name='removestore'),
    url(r'^removemember',views.removemember,  name='removemember'),
    url(r'^checkmember',views.checkmember,  name='checkmember'),
    url(r'^checkstore',views.checkstore,  name='checkstore'),
]

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










































