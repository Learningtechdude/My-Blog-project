from unicodedata import category
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Contact, Post, AboutUs, Category

class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    message = forms.CharField(label='Message', required=True)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username',max_length=100, required=True)
    email = forms.EmailField(label='Email',max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(),label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput(),label='Confirm password')

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password do not Match")

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            self.user = user

class NewPostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200, required=True)
    content = forms.CharField(widget=forms.Textarea, label='Content', required=True)
    upload_img_url = forms.ImageField(required=False)
    external_img_url = forms.URLField(required=False)
    category = forms.ModelChoiceField(label='Category', required=True, queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'content', 'upload_img_url', 'external_img_url', 'category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.") 
        if content and len(content) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.")