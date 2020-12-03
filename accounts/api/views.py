from rest_framework.generics import CreateAPIView,RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from .serializers import UserCreateSerializer,UserSerializer

User=get_user_model()

#view for creating user
class UserCreateAPIView(CreateAPIView):
    
    queryset=User.objects.all()
    serializer_class=UserCreateSerializer
    permission_classes=[AllowAny]


#view for retrieving user
class UserRetrieveAPIView(RetrieveAPIView):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    #Before changing this,edit code below
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        
        #overriding get_object() method to retrive user
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset,id=self.request.user.id)
        return obj