from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('profile/', views.profile, name="profile"),
    path('auth/register/', views.register_view, name="register"),
    path('auth/login/', views.login_view, name="login"),
    path('auth/logout/', views.logout_view, name="logout"),
    path('create_post/', views.create_post, name="create_post"),
    path('delete_post/<int:id>', views.delete_post, name="delete_post"),
    path('showuser/<int:id>', views.showuser, name="showuser"),
    path('follow/<int:id>', views.follow, name="follow"),
    path('unfollow/<int:id>', views.unfollow, name="unfollow"),
    path('post/<int:id>', views.post, name="post"),
    path('add_comment/<int:postid>', views.add_comment, name="add_comment"),
    path('like_post/<int:postid>', views.like_post, name="like_post"),
    path('unlike_post/<int:postid>', views.unlike_post, name="unlike_post"),
]

if settings.DEBUG:
    #connecting Media url to Media dir
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
