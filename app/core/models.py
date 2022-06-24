from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fieds):
        """ Creates and saves a new User """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email = self.normalize_email(email),**extra_fieds)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        """Create and saves super user"""
        user = self.create_user(email,password)
        user.is_staff=True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """ Custom user model that suppors using email instead of username """
    email = models.EmailField(max_length=255,unique = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
