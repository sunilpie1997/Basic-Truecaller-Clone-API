from django.urls import path
from .views import UserCreateAPIView,UserRetrieveAPIView




#add user update view if have time
urlpatterns=[

    path('',UserRetrieveAPIView.as_view(),name='get-user'),

    path('create/',UserCreateAPIView.as_view(),name='create-user'),

]
    