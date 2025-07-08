from django.contrib import admin
from django.urls import path
from accounts.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(),name="token_refresh"), 
    
    path("register/",register_user,name="register"),
    path('users/',user_list,name='user-list'),
    path('users/<uuid:pk>/',user_detail,name='user-detail'),
    path('users/<uuid:pk>/update/',user_update,name='user-update'),
    path('users/<uuid:pk>/delete/',user_delete,name='user-delete'),

    path("group/",group_list,name='group_list'),
    path('group/create/',group_create,name='group_crate'),
    path('group/<int:pk>/detail/',group_detail,name='group_detail'),
    path('group/<int:pk>/update/',group_update,name='group_update'),
    path('group/<int:pk>/delete',group_delete,name='group_delete'),

    path('permission/',permission_list_view,name='permission'),
]