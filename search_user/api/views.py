from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from search_user.models import PhoneDirectory,isPhoneNumberValid
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import re
from .serializers import UnknownNumberSerializer,RegisteredNumberSerializer,RegisteredNumberByUnknown#intentionally done

User=get_user_model()


#increase spam_score of 'phone number' in 'PhoneDirectory'
class AddToSpamView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):

        
        phone=request.data.get('phone',None)
        if phone is None:
            return Response(data={"detail":"phone number is required"},status=status.HTTP_400_BAD_REQUEST)

        else:
            if isPhoneNumberValid(phone):

                obj,is_created=PhoneDirectory.objects.get_or_create(phone=phone)
                obj.updateSpamScore()
                obj.save()
                return Response(status=status.HTTP_200_OK)

            else:

                return Response(data={"detail":"enter valid phone number"},status=status.HTTP_400_BAD_REQUEST)


#search user by 'phone number'
class SearchUserByPhoneView(APIView):

    #before changing this to unauthenticated,add additional check in below code as request.user will return None
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):

        phone=request.data.get('phone',None)
        #if 'phone' is not present in request body
        if phone is None:
            return Response(data={"detail":"phone number is required"},status=status.HTTP_400_BAD_REQUEST)
            
        else:

            #check if 'phone number' is valid
            if isPhoneNumberValid(phone):
                
                #get 'phone number' object from 'PhoneDirectory' to check 'is_registered' property
                phone_object=get_object_or_404(PhoneDirectory,phone=phone)

                #if 'phone number' is registered
                if phone_object.does_user_exist():

                    get_user_by_phone=phone_object.getRegisteredUser()
                    user=get_object_or_404(User,username=request.user.username)
                    
                    if (get_user_by_phone.contact_list is not None and get_user_by_phone.contact_list.isPhoneInContactList(user.get_username())) or get_user_by_phone.get_username()==user.get_username():

                        serialized_object=RegisteredNumberSerializer(phone_object)
                        #response with email as user who is searching is in 'contact_list'
                        return Response(data=serialized_object.data,status=status.HTTP_200_OK)
                    else:
                        #response without email
                        serialized_object=RegisteredNumberByUnknown(phone_object)
                        return Response(data=serialized_object.data,status=status.HTTP_200_OK)

                #if 'phone number' is not registered
                else:
                    serialized_object=UnknownNumberSerializer(phone_object)
                    return Response(data=serialized_object.data,status=status.HTTP_200_OK)

            else:
                return Response(data={"detail":"enter valid phone number"},status=status.HTTP_400_BAD_REQUEST)


"""
#search user by name
class SearchUserByNameView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):

        first_name=request.data.get('first_name',None)
        last_name=request.data.get('last_name',"")

        if first_name is None:
            return Response(data={"detail":"first_name is required"},status=status.HTTP_400_BAD_REQUEST)
            
        else:

            if isNameValid(first_name) and isNameValid(last_name):
                PhoneDirectory.objects.filter(name_list__="")

            else:
                return Response(data={"detail":"each name should be not more than 20 chars"},status=status.HTTP_400_BAD_REQUEST)
"""