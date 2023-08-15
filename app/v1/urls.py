from django.urls import path, include
from .accounts import views as accountViews
from .posts import views as postViews
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'account', accountViews.AccountViewset)
router.register(r'post', postViews.PostViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('account/refresh/', TokenRefreshView.as_view()) # POST {refresh : str} => {access : str}
]
