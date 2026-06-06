from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    upload_img_url = models.ImageField(upload_to='posts/', null=True, blank=True)
    external_img_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property        
    def img_url(self):
        if self.upload_img_url:
            return self.upload_img_url.url
        elif self.external_img_url:
            return self.external_img_url
        return ""
        
    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()