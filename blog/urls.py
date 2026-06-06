from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.index, name = "index"),
    path('post/<slug:slug>/', views.detail, name = "detail"),
    path('new_something_url/', views.new_url_view, name = "new_page_url"),
    path('old_url/', views.old_url_redirect, name = "old_url"),
    path('contact/', views.contact_view, name = "contact"),
    path('about/', views.about_us, name = "about"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout/',views.logout_view,name="logout"),
    path('new_post/',views.new_post,name="new_post"),
    path('edit_post/<int:post_id>/',views.edit_post,name="edit_post"),
    path('delete_post/<int:post_id>/',views.delete_post,name="delete_post"),
    path('publish_post/<int:post_id>/',views.publish_post,name="publish_post")
]