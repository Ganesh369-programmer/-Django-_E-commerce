from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# AbstractBaseUser ;- this is Base class for custom User
# BaseUserManager ;- it is helps to create the user properly (just like providing validation email , and hash Passward )
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self , first_name , last_name , username , email , password=None):

        if not email:
            raise ValueError('User must have an email address ')
        
        if not username:
            raise ValueError(' User must have an Username ')
        
        #self.model :- refer to custom model , it creates new user objects in memory
        #normalize_email :- it is use for convert the mail , from/ GANESH@GMAIL.COM → ganesh@gmail.com

        user = self.model(
            email = self.normalize_email(email),
            username = username , 
            first_name = first_name , 
            last_name = last_name ,

        )

        #set_password ;- it convert password in hash for security 
        user.set_password(password)
        user.save(using=self.__db)
        return user


    def create_superuser(self , first_name , last_name , email , username , password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username , 
            password = password , 
            first_name = first_name , 
            last_name= last_name ,
        )

        #is_admin :- used to identify admin level user ,
        user.is_admin = True

        #is_active :- it indicate the user is activate or not , user cannot login 
        user.is_active = True

        #is_staff :- it allows to access django admin panel
        user.is_staff = True\
        
        #is_superadmin :- it gives the permission , to perform add , update , delete 
        user.is_superadmin = True
        user.save(using = self._db)
        return user

    



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50 , unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    phone_number = models.CharField(max_length=50) 

    #required 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self , perm , obj = None):
        return self.is_admin

    def has_module_perms(self , add_label):
        return True    
