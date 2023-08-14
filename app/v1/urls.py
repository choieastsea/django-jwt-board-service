from django.contrib import admin
from django.urls import path, include
from .accounts import views as accountViews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'account', accountViews.AccountViewset)

urlpatterns = [
    path('', include(router.urls)),
]
