from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.navigate, name='navigate'),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('index/',views.index, name="index"),
    path('logout/',views.logout,name="logout"),
    path('token/',views.token_send,name="token_send"),
    path('success/',views.success,name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
    path('readmore/<int:id>',views.readmore,name='readmore'),
    path('friend_list/',views.friend_list,name="friend_list"),
    path('friend_request/',views.friend_request,name='friend_request'),
    path('add-friend/<int:id>/',views.send_request,name='add-friend'),
    path('accept/<int:id>/',views.accept_request,name='accept'),
    #path('accept_friend_request/<int:id>',views.accept_friend_request,name='accept_friend_request'),
    #path('cancle_friendrequest/',views.cancle_friendrequest,name='cancle_friendrequest'),
    #path('add_friend/<int:id>',views.add_friend,name='add_friend'),
    ####reset password########
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    #####################Admin panel######################################
    path('admin_login',views.admin_login, name='admin_login'),
    path('fbadmin/admin_panel',views.admin_panel, name='admin_panel'),
    path('fbadmin/users',views.users, name='users'),
    path('fbadmin/admin_image',views.admin_image, name='admin_image'),
    path('fbadmin/admin_coment',views.admin_coment, name='admin_coment'),
    path('fbadmin/admin_flist',views.admin_flist, name='admin_flist'),
    path('fbadmin/admin_frequest',views.admin_frequest, name='admin_frequest'),
    path('fbadmin/admin_certificate', views.admin_certificate, name='admin_certificate'),
    path('fbadmin/admin_prediator', views.admin_prediator, name='admin_prediator'),
    path('fbadmin/admin_imgprediator', views.admin_imgprediator, name='admin_imgprediator'),
]