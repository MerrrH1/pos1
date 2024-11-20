from django.contrib import admin
from pos_app.models import (
    User, StatusModel, TableResto, Profile, Category, MenuResto,OrderMenu, OrderMenuDetail
)

admin.site.register(User)
admin.site.register(StatusModel)
admin.site.register(TableResto)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(MenuResto)
admin.site.register(OrderMenu)
admin.site.register(OrderMenuDetail)