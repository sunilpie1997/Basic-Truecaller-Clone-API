
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import homePage

urlpatterns = [
    path('',homePage,name="homepage"),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/',include("accounts.api.urls")),
    path('caller/',include("search_user.api.urls"))
    
]
