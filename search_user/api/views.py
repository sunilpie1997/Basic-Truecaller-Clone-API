from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from search_user.models import PhoneDirectory,isPhoneNumberValid,isNameValid
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import re
from accounts.models import ContactList
from .serializers import PhoneDirectorySerializer,UnknownNumberSerializer,RegisteredNumberSerializer,RegisteredNumberByUnknown#intentionally done

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
                #'get()' will return only one row as it has OneToOne relation with 'User' model  
                user_data=get_object_or_404(ContactList,user=request.user)
                #is phone already in spam_list of user
                if user_data.isPhoneInSpamList(phone):
                    #if yes DON'T DO ANYTHING
                    return Response(status=status.HTTP_200_OK)
                
                else:
                    #update spam_score and also add this 'phone no' to spam_list of user
                    obj,is_created=PhoneDirectory.objects.get_or_create(phone=phone)
                    obj.updateSpamScore()
                    obj.save()
                    user_data.addPhoneToSpamList(phone)
                    user_data.save()
                    return Response(status=status.HTTP_200_OK)

            else:

                return Response(data={"detail":"enter valid phone number"},status=status.HTTP_400_BAD_REQUEST)


#search user by 'phone number'
class SearchUserByPhoneView(APIView):

    #before changing this to unauthenticated,please place additional check in below code as request.user will return None
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):

        phone=request.query_params.get('phone',None)
        #if 'phone' is not present in request body
        if phone is None:
            return Response(data={"detail":"phone number is required"},status=status.HTTP_400_BAD_REQUEST)
            
        else:

            #check if 'phone number' is valid
            if isPhoneNumberValid(phone):
                
                #get 'phone number' object from 'PhoneDirectory'
                phone_object=get_object_or_404(PhoneDirectory,phone=phone)

                #if 'phone number' is registered
                if phone_object.does_user_exist():

                    get_user_by_phone=phone_object.getRegisteredUser()
                    user=get_object_or_404(User,id=request.user.id)
                    
                    #if user who is requesting is in 'contact_list' of 'phone_no.' user or they both are same
                    if (get_user_by_phone.contact_list is not None and get_user_by_phone.contact_list.isPhoneInContactList(user.get_username())) or get_user_by_phone==user:

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



#search user by first_name
class SearchUserByNameView(APIView):

    #before changing this to unauthenticated,please place additional check in below code as request.user will return None
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):

        first_name=request.query_params.get('first_name',None)
        last_name=request.query_params.get('last_name',None)

        #if first_name is None
        if first_name is None:
            return Response(data={"detail":"first_name is required"},status=status.HTTP_400_BAD_REQUEST)
            
        else:
            #if first_name is valid and ((last_name is not None and valid) or last_name is None)
            if isNameValid(first_name) and ((last_name is not None and isNameValid(last_name)) or last_name is None):
                user=get_object_or_404(User,id=request.user.id)
                
                if last_name is not None:

                    #filter by first_name and last_name
                    list_of_users=(PhoneDirectory.objects.filter(name_list__icontains=first_name) & PhoneDirectory.objects.filter(name_list__icontains=last_name))[0:20].select_related('user')
                else:
                    #filter by first_name
                    list_of_users=PhoneDirectory.objects.filter(name_list__icontains=first_name)[0:20].select_related('user')
                
                #serialize list of 'phone_no' objects of type 'PhoneDirectory'
                serialized_list=PhoneDirectorySerializer(list_of_users,many=True)
                
                #set email ="" , if requesting user not in contact_list of 'phone_no' user
                #Filtering
                for each in serialized_list.data:
                    #get 'phone_no' user 
                    phone_user=each.get('user',None)
                    #if above is not None
                    if phone_user is not None:
                        #get contact_list of above
                        contact_list=phone_user.get("contact_list").get("data")
                        #check if requesting user's phone no(technically username) exists in contact_list
                        if user.get_username() in contact_list:
                            user_email=phone_user.get("email")
                            #set email property 
                            each["email"]=user_email
                        #delete user property (not required)
                        del each["user"]

                    #for each name in name_list, that contains first_name or/and last_name, add it to serialized data in form of list
                    li=[]
                    name_list=each.get("name_list")
                    for name in name_list:
                        #if last_name is not None ,regex match using both names
                        if last_name is not None and re.match('[a-zA-Z]*('+first_name+')\s*[a-zA-Z]*('+last_name+')[a-zA-Z]*',name,re.IGNORECASE) is not None:
                            li.append(name)
                        
                        #if last_name is None,regex match using only first_name
                        elif re.match('[a-zA-Z]*('+first_name+')[a-zA-Z]*',name,re.IGNORECASE) is not None:
                            li.append(name)
                    #overwrite 'name_list' property
                    each["name_list"]=li.copy()
                            

                return Response(data=serialized_list.data,status=status.HTTP_200_OK)


            else:
                return Response(data={"detail":"each name should be not more than 20 chars"},status=status.HTTP_400_BAD_REQUEST)
