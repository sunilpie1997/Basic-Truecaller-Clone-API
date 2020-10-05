from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from search_user.models import PhoneDirectory
import re

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


#return empty 'dict' for each model instance of type 'ContactList'
def returnEmptyDict():
    return {}


def validateNameLength(value):
    if len(value)<=100:
        return True
    else:
        return False

    

#custom user model
class  User(AbstractUser):
    
    username=models.CharField(max_length=20,null=False,validators=[isPhoneNumberValid],blank=False,unique=True,db_index=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    first_name=models.CharField(max_length=100,blank=False,null=False)
    last_name=models.CharField(max_length=100,default="",blank=True)
    #last_name wiil be automatically added 'blank=True,null=True,max_length>=100'


    def setLastName(self,last_name):
        if isinstance(last_name,str) and validateNameLength(last_name):
            self.last_name=last_name
        else:
            raise TypeError('{name} should be a {typeOf} ({length} chars)'.format(name="last_name",length=100,typeOf="string"))


    def getLastName(self):
        return self.last_name


    def getFirstName(self):
        return self.first_name

    
    def __str__(self):
        return '{first_name} with {number}'.format(first_name=self.first_name,number=self.username)


#model to store 'contact-list' of each user
class ContactList(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="contact_list",primary_key=True)
    data=models.JSONField(default=returnEmptyDict,blank=True)


    #get contact_list of user
    def getContacts(self):
        return self.data


    #to check if given 'phone number' is in the contact list
    def isPhoneInContactList(self,phone_no):
        contact_list=self.getContacts()
        if contact_list.get(phone_no,None) is None:
            return False
        else:
            return True

    
    #add contact to contactList
    def addPhoneToContactList(self,phone_no):
        if isinstance(phone_no,dict):
            contact_list=self.getContacts()
            contact_list.update(phone_no)
        
        else:
            raise TypeError('{name} should be a {typeOf}'.format(name="phone_no",typeOf="dictionary"))


    def __str__(self):
        return str(self.user)



#whenever user is created or saved,global phone directory should be updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_phone_directory(sender, instance, created, update_fields, **kwargs):

    phoneObject,is_created=PhoneDirectory.objects.get_or_create(phone=instance.username)
    phoneObject.setUser(instance)
    list_of_names=phoneObject.getNameList()
    list_of_names.update({instance.getFirstName():instance.getFirstName()})

    phoneObject.save()

    if created:
        ContactList.objects.create(user=instance)

    instance.contact_list.save()


#whenever registered 'user' is deleted, update 'PhoneDirectory' to set 'user'= None
@receiver(post_delete,sender=settings.AUTH_USER_MODEL)
def update_phone_directory(sender,instance,**kwargs):

    phoneObject,is_created=PhoneDirectory.objects.get_or_create(phone=instance.username)
    phoneObject.setUserNone()

    phoneObject.save()