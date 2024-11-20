from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    TableRestoListApiView, TableRestoDetailApiView, CategoryListApiView, CategoryDetailApiView, MenuRestoListApiView,
    MenuRestoDetailApiView, RegisterUserApiView, LoginView, MenuRestoView
)

app_name = "api"

urlpatterns = [
    path('api/register', RegisterUserApiView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/table_resto', views.TableRestoListApiView.as_view()),
    path('api/table_resto/<int:id>', views.TableRestoDetailApiView.as_view()),
    path('api/category', views.CategoryListApiView.as_view()),
    path('api/category/<int:id>', views.CategoryDetailApiView.as_view()),
    path('api/menu_resto', views.MenuRestoListApiView.as_view()),
    path('api/menu_resto/<int:id>', views.MenuRestoDetailApiView.as_view()),
    path('api/menu-resto', views.MenuRestoView.as_view()),
]