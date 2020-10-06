from rest_framework.serializers import ModelSerializer
from search_user.models import PhoneDirectory
from accounts.models import ContactList
from django.contrib.auth import get_user_model

User=get_user_model()

class UserWithEmailSerializer(ModelSerializer):

    class Meta:
        model=User
        fields=["first_name","last_name","email"]


class UserWithoutEmailSerializer(ModelSerializer):

    class Meta:
        model=User
        fields=["first_name","last_name"]


#This serializer is used to serialize data (in case of unregistered phone numbers)
class UnknownNumberSerializer(ModelSerializer):

    class Meta:
        model=PhoneDirectory
        fields=["phone","name_list","spam_score"]


class RegisteredNumberSerializer(ModelSerializer):

    user=UserWithEmailSerializer()
    class Meta:
        model=PhoneDirectory
        fields=["phone","name_list","spam_score","user"]


#if user searches for registered number,but he/she is not present in his/her contact_list
class RegisteredNumberByUnknown(ModelSerializer):

    user=UserWithoutEmailSerializer()
    class Meta:
        model=PhoneDirectory
        fields=["phone","name_list","spam_score","user"]


class ContactListSerializer(ModelSerializer):

    class Meta:
        model=ContactList
        fields=["data"]


class CompleteUserSerializer(ModelSerializer):

    contact_list=ContactListSerializer()
    class Meta:
        model=User
        fields=["first_name","last_name","email","contact_list"]
    

class PhoneDirectorySerializer(ModelSerializer):

    user=CompleteUserSerializer()
    class Meta:
        model=PhoneDirectory
        fields=["phone","spam_score","name_list","user"]