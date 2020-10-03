from django.urls import path
from .views import AddToSpamView,SearchUserByPhoneView




urlpatterns=[

    path('add_to_spam/',AddToSpamView.as_view(),name='add-to-spam'),
    path('search_by_phone/',SearchUserByPhoneView.as_view(),name='search-by-phone')

]
    