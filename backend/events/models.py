from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
        
# Addition of code
# Reason - crete a model to manage user and superuser
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)
# End of addition of code
# Reason - crete a model to manage user and superuser  

# Addition of code
# Reason - crete a model to store user and superuser  
class User(AbstractBaseUser):
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other'),
        ('N/A', 'Prefer not to say')
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES,blank=True,null=True,)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """Return True if the user has a specific permission."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the app `app_label`."""
        return self.is_superuser
    class Meta:
        verbose_name_plural = "User"
        
    USERNAME_FIELD = 'username'    
    REQUIRED_FIELDS = ['email', 'first_name', 'contact_number']
    
# End of addition of code
# Reason - crete a model to store user and superuser      
        
# Addition of code
# Reason - crete a model to store Events         
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey('User', on_delete=models.CASCADE, related_name="organized_events")
    rsvp_limit = models.PositiveIntegerField(null=True, blank=True) 
    rsvp_count = models.PositiveIntegerField(null=True, blank=True)
    
    def clean(self):
        if self.rsvp_limit is None:
            self.rsvp_limit = 99999  

    class Meta:
        ordering = ['date', 'time']  

    def __str__(self):
        return f"{self.title}"
# End of addition of code
# Reason - crete a model to store Events        

# Addition of code
# Reason - crete a model to store category of Events       
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
# End of addition of code
# Reason - crete a model to store category of events 
  
class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if RSVP.objects.filter(user=self.user, event=self.event).exists():
            raise ValidationError("An RSVP with this user and event already exists.")
        
        if self.event.rsvp_limit is not None:
            rsvp_count = RSVP.objects.filter(event=self.event).count()
            if rsvp_count >= self.event.rsvp_limit:
                raise ValidationError(f"Cannot RSVP, the event has reached its RSVP limit of {self.event.rsvp_limit}.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)  
        if self.event.rsvp_count is None:
            self.event.rsvp_count = 1  
        else:
            self.event.rsvp_count += 1  

        self.event.save() 

        

    def __str__(self):
        return f"{self.user.username} RSVP'd for {self.event.title}"
