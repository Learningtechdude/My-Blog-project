from django.contrib import admin
from .models import Contact, Post, Category, AboutUs
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted')
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(AboutUs)
admin.site.register(Contact)