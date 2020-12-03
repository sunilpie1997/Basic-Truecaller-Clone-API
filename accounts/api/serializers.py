from rest_framework.serializers import ModelSerializer,RegexField,CharField,EmailField
from rest_framework.validators import UniqueValidator
from accounts.models import ContactList
from django.contrib.auth import get_user_model

User=get_user_model()

#to create user
class UserCreateSerializer(ModelSerializer):
    
    #username is in the form of '10 digit phone no'
    username = RegexField(regex=r'^[1-9][0-9]{9}$',required=True,validators=[UniqueValidator(queryset=User.objects.all(),message="Account with this contact no already exists")])
    first_name = RegexField(required=True,regex=r'^[a-zA-Z]{3,20}$')
    
    #not required
    last_name=RegexField(required=False,regex=r'^[a-zA-Z]{3,20}$')
    password=CharField(required=True,write_only=True,max_length=50,min_length=8)
    
    #not required
    email=EmailField(required=False,max_length=50)

    class Meta:
        model=User
        fields=["username","first_name","last_name","password","email"]
    

    """
    need to override create method to store password in hash form
    """
    def create(self,validated_data):
        new_username=validated_data.get("username")
        new_firstname=validated_data.get("first_name")
        new_lastname=validated_data.get("last_name","")#blank if not provided
        new_email=validated_data.get("email","")#blank if not provided
        new_password=validated_data.get("password")

        new_user=User.objects.create_user(username=new_username,password=new_password,first_name=new_firstname,email=new_email,last_name=new_lastname)
        return new_user


#to retrieve user
class UserSerializer(ModelSerializer):

    class Meta:
        model=User
        fields=["username","email","first_name","last_name"]
