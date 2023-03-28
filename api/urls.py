from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.urls import path

from core.views import MyTokenObtainPairView


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]