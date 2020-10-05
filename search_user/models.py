from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import re




#check if 'name' entered by user for search in global database is valid
def isNameValid(name):
    if isinstance(name,str) and len(name)<=20:
        return True
    else:
        return False


#for now,only Indian numbers are supported
def isPhoneNumberValid(phone):
    if isinstance(phone,str) and len(phone)==10:
        result=re.search('^[1-9][0-9]{9}$',phone)
        if result is None:
            return False
        else:
            return True
    else:
        return False
        

#return empty 'dict' for each model instance
def returnEmptyDict():
    return {}


class PhoneDirectory(models.Model):
    
    phone=models.CharField(max_length=20,validators=[isPhoneNumberValid],null=False,blank=False,unique=True,db_index=True)
    spam_score=models.BigIntegerField(default=0)
    name_list=models.JSONField(default=returnEmptyDict,blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="directory")


    def updateSpamScore(self):
        self.spam_score=self.spam_score+1


    def getPhoneNo(self):
        return self.phone
    
    
    def getSpamScore(self):
        return self.spam_score


    def getNameList(self):
        return self.name_list


    def does_user_exist(self):
        if self.user is None:
            return False
        else:
            return True


    def setUserNone(self):
        self.user=None


    def getRegisteredUser(self):
        return self.user


    def setUser(self,phone_user):
        if isinstance(phone_user,AbstractUser):
            self.user=phone_user
        
        else:
            raise TypeError('{name} should be of type {typeOf}'.format(name="phone_user",typeOf="User"))


    def __str__(self):
        return str(self.phone)+" spam_score:"+str(self.spam_score)
