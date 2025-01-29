from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import FriendshipRequestManager
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    avatar = models.ImageField(blank=True, null=True)
    rank = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    country = models.CharField(max_length=100, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friend_of', blank=True)
    blocked_users = models.ManyToManyField('self',symmetrical=False, related_name='blocked_by', blank=True)

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        #Avatar image resize
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 600 or img.width > 600:
                output_size = (600,600)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
                #SENEM: kullanıcı yeni avatar eklediğinde eski avatarı silmek için koda ekleme yapmalısın!!




# Arkadaşlık İsteği Modeli
class FriendshipRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, blank=False, null=False)

    STATUS_CHOICES = [
        ('P', 'Beklemede'),
        ('A', 'Kabul Edildi'),
        ('R', 'Reddedildi'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='P') # status kaldırılabilir çok şart değil
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    objects = FriendshipRequestManager()

    def clean(self):
        self.__class__.objects.create_friendship_request(self.sender, self.receiver, self.status)

    def save(self, *args, **kwargs):
        existing_request = FriendshipRequest.objects.filter(
                sender=self.sender,
                receiver=self.receiver,
                is_active=True
            )
        if existing_request.exists():
            if self.status == 'A':
                existing_request.update(status=self.status, is_active=False)
                self.sender.friends.add(self.receiver)
            if self.status == 'R':
                existing_request.update(status=self.status, is_active=False)
            if self.is_active == False:
                existing_request.update(is_active=False)
        else:
            super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.sender.username} sent friendship request to the {self.receiver.username}"

