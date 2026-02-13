from django.urls import path

from apps.user import views as user_views
from rest_framework_simplejwt import views as rest_framework_views

urlpatterns = [
    path("signup/", user_views.SignupView.as_view(), name="signup"),
    path("login/", rest_framework_views.TokenObtainPairView.as_view(), name="login"),
    path(
        "token/refresh/",
        rest_framework_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("me/", user_views.UserView.as_view(), name="user_profile"),
    path(
        "purchase-history/",
        user_views.PurchaseHistoryView.as_view(),
        name="purchase_history",
    ),
]
