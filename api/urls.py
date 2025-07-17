from django.urls import path
from .views import category_views

urlpatterns = [
    path("categories/create/",category_views.category_create,name="category-create"),
    path("categories/list/",category_views.category_list,name="category_list"),
    path("categories/<uuid:pk>/",category_views.category_detail,name="category_detail"),
    path("categories/<uuid:pk>/update/",category_views.category_update,name="category_update"),
    path("categories/<uuid:pk>/delete/",category_views.category_delete,name="category_delete"),
   
]