from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notes = models.ManyToManyField(Note)
    
    def __str__(self):
        return self.user.username
    
    """ signals!!Methods that creates an instance in UserProfile when a user is created. Either by registration or google """
    
    # Method that connects to the "post_save" signal of the User model and creates an instance of UserProfile associated with the newly created user.

    @classmethod
    def create_user_profile(cls, sender, instance, created, **kwargs):
        if created:
            cls.objects.create(user=instance)
    
    # Method connected to the same signal that ensures that the UserProfile instance is saved whenever the User model is saved.

    @classmethod
    def save_user_profile(cls, sender, instance, **kwargs):
        instance.userprofile.save()

post_save.connect(UserProfile.create_user_profile, sender=User)
post_save.connect(UserProfile.save_user_profile, sender=User)
